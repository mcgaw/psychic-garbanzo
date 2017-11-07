import numpy as np
import subprocess

INF = float('Inf')

for _ in range(100000):
    n = 3353
    FILE = 'rome.txt'

    s = np.random.randint(1, n)
    t = np.random.randint(1, n)

    results = []
    for prog in ['./dist_preprocess_small.sh', './dist_no_preprocess_small.sh']:
        print(s, ' -> ', t)
        proc = subprocess.Popen([prog], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

        with open(FILE) as file:
            line = file.read()
            while line:
                print(line, file=proc.stdin)
                line = file.read()

        print(1, file=proc.stdin)
        print(s, ' ', t, file=proc.stdin)

        stdoutdata, _ = proc.communicate()
        assert proc.returncode == 0

        stdout_lines = stdoutdata.splitlines()
        results.append(stdout_lines[1])
        print(stdoutdata, end='')

    assert results[0] == results[1], '{0} {1}'.format(results[0], results[1])
