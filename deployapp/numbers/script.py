
import sys
import classifier

if __name__ == '__main__':
    """Script should be called with one argument: path to input file.
    The input file should be line-delimited and contain only numbers.
    The output is written to a file named 'result.data'."""

    with open(sys.argv[1]) as f:
        values = (int(line) for line in f)
        results = classifier.classify(values)
    
    with open('result.data', 'w') as outf:
        for result in results:
            outf.write(result + '\n')
     
