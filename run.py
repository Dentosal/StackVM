import sys
from stackvm import vm

vm.main(sys.argv[1], debug=("--debug" in sys.argv), slow=("--slow" in sys.argv))
