import re
import numpy as np
import matplotlib.pyplot as plt

def extract_cirs(log):
    """Extract CIR measurement results

    Parameters
    ----------
    log: str
        log file loaded into a string

    Returns
    -------
    cirs: list
        list of tuples (cir - ndarray [ts, cir], cir_header - dict)
    """
    cir_pattern = r"((RX OK.*\n.*\n)(([-\d]+,[-\s\d]+\n)+))"
    cirs_logs = re.findall(cir_pattern, log)

    cirs = []

    for x, i in zip(cirs_logs, range(len(cirs_logs))):
        # get cir header
        header = x[1]
        cir_header_values = [x.replace('(', '').replace(')', '') for x in re.findall(r'\([\d\w\s\-\.]+\)', header)]
        cir_header_keys = ['WInd', 'HLP', 'PSC', 'SLP', 'RC', 'DCR', 'DCI', 'NTH', 'T', 'RSL', 'FSL', 'RSMPL']
        cir_header = {k: v for k, v in zip(cir_header_keys, cir_header_values)}

        # convert first path detection ts to float
        cir_header['HLP'] = float(cir_header['HLP'])

        # compute cir
        cir = x[2].replace('\n\n', '').split('\n')
        if not len(cir[-1]):
            cir = cir[:-1]

        cir = [np.linalg.norm(np.array(x.split(',')).astype('int')) for x in cir]
        ts = np.arange(len(cir)) - cir_header['HLP']
        cir = np.c_[ts, cir]

        cirs.append((cir, cir_header))
    return cirs


def extract_tofs(log):
    """Extract ToF measurement results

    Parameters
    ----------
    log: str
        log file loaded into a string

    Returns
    -------
    dist: ndarray
        distance measurements in meters
    """
    dist_pattern = r"Dist: [\d\.]+ m"
    tof_lines = re.findall(dist_pattern, log)

    dist = np.array([float(x.split(' ')[1]) for x in tof_lines])
    return dist



def main():
    """
    Main function
    Returns
    -------

    """
    # load file 1
    file_id = 1
    with open('results/{}.log'.format(file_id), 'r') as f:
        log = f.read()

    # extract CIRs
    cirs = extract_cirs(log)

    # extract ranging results
    dist = extract_tofs(log)

    # plot exemplary CIR
    c = cirs[0][0]
    plt.plot(c[:,0],c[:,1])
    plt.title('CIR')
    plt.show()

    # plot exemplary distance measurements
    plt.plot(dist)
    plt.title('distance [m]')
    plt.show()


if __name__ == "__main__":
    main()


