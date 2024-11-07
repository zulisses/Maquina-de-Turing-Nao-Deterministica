import json
import sys
import os
import time

class TuringMachine:
    
    def __init__(self, data):
        self.states = data[0]
        self.input_alphabet = data[1]
        self.tape_alphabet = data[2]
        self.start_marker = data[3]
        self.blank_marker = data[4]
        
        self.transitions = {}
        for transition in data[5]:
            if (transition[0], transition[1]) not in self.transitions:
                self.transitions[(transition[0], transition[1])] = []
            self.transitions[(transition[0], transition[1])].append(transition[2:5])

        self.initial_state = data[6]
        self.final_states = data[7]

    def word_validation(self, word) -> bool:
        for ch in word:
            if(ch not in self.input_alphabet):
                return False
        return True
    
    def run(self, word) -> int:

        if not self.word_validation(word): 
            return False
        
        word = self.start_marker + word
        stack = [(self.initial_state, 1, word)]

        counter = 0
        while len(stack):
            counter += 1
            (curr_state, curr_head, word) = stack.pop(0)
            
            # os.system('clear')
            # print(f"{counter} Estado: {curr_state} - Palavra: {word}")
            # time.sleep(0.003)

            if(curr_head == -1): return False

            if(curr_head == len(word)):
                word += self.blank_marker

            possible_exit = True

            transitions = self.transitions.get((curr_state, word[curr_head]))
            if transitions:
                for (next_state, superscript_symbol, direction) in transitions:
                    word = word[0:curr_head] + superscript_symbol + word[curr_head+1:len(word)]
                    stack.append((next_state, curr_head + 1 if direction == '>' else curr_head - 1, word))
                    possible_exit = False

            if possible_exit and curr_state in self.final_states:
                return True
        
        return False

if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print("Usar: python3 mt.py [MT] [Palavra]")
        sys.exit(1)

    json_file = sys.argv[1]
    word = sys.argv[2]

    with open(json_file, 'r') as file:
        data = json.load(file)

    mt = TuringMachine(data['mt'])

    print("Sim" if mt.run(word) else "Não")