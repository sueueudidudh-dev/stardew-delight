"""Builds every target (or the ones given) one by one and prints a summary.

  python dev/build_all.py                  all targets from settings.gradle.kts
  python dev/build_all.py 1.21.1-fabric    only these

Each target runs as its own Gradle invocation (dev/gw.bat :<target>:buildAndCollect), so one broken target does not
stop the others. Logs go to build/logs/<target>.log, jars to build/libs/<mod version>/.
"""
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def targets():
    text = open(os.path.join(ROOT, 'settings.gradle.kts'), encoding='utf-8').read()
    out = []
    for version, loaders in re.findall(r'^\s*match\("([^"]+)",\s*([^)]+)\)', text, re.M):
        for loader in re.findall(r'"([a-z]+)"', loaders):
            out.append(f'{version}-{loader}')
    return out


def main():
    wanted = sys.argv[1:] or targets()
    logs = os.path.join(ROOT, 'build', 'logs')
    os.makedirs(logs, exist_ok=True)
    results = []
    for t in wanted:
        start = time.time()
        log = os.path.join(logs, f'{t}.log')
        with open(log, 'w', encoding='utf-8', errors='replace') as f:
            code = subprocess.call(['cmd', '/c', os.path.join(ROOT, 'dev', 'gw.bat'), f':{t}:buildAndCollect'],
                                   cwd=ROOT, stdout=f, stderr=subprocess.STDOUT)
        text = open(log, encoding='utf-8', errors='replace').read()
        errors = re.findall(r'^.*\.java:\d+: error: .*$', text, re.M)
        wrong = re.findall(r'\* What went wrong:\n(.*(?:\n.*){0,3})', text)
        status = 'OK' if code == 0 else 'FAILED'
        results.append((t, status, time.time() - start))
        print(f'{t:16} {status:6} {time.time() - start:6.0f}s  {log}', flush=True)
        for e in errors[:15]:
            print('    ' + e.strip()[:240])
        if code != 0 and not errors:
            for w in wrong[:2]:
                print('    ' + w.strip().replace('\n', ' | ')[:400])
    print()
    print('OK:', sum(1 for r in results if r[1] == 'OK'), 'of', len(results))


if __name__ == '__main__':
    main()
