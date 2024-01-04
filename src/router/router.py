from parsers import PracticalFormatParser

print("Hello")

pFP = PracticalFormatParser()

file = open("benchmarks\counter7.txt", 'r')

pFP.parse_file(file)