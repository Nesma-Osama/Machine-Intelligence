from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []
        #######################Variables##########################
        # get the unique letters from the equation
        all_letters = list(set(LHS0 + LHS1 + RHS))
        # convert the set into to list
        problem.variables.extend(all_letters)
        # the max length of the two LHS terms
        max_columns=max(len(LHS0),len(LHS1))
        # Carrier variables for each column
        carry_vars = [f'C{i}' for i in range(max_columns+1)]
        # Add the carrier variables to the problem
        problem.variables.extend(carry_vars)
        #######################Domains##########################
        ## domain of the letters
        for letter in all_letters:
            problem.domains[letter] = set(range(10))
        ## domain of the carrier variables
        for c in carry_vars:
            problem.domains[c] = set(range(2))  # carry can be either 0 or 1
        # Unary Constraints
        # Variables
        problem.constraints.append(UnaryConstraint(LHS0[0], lambda x: x != 0))  # First letter of LHS0 cannot be 0
        problem.constraints.append(UnaryConstraint(LHS1[0], lambda x: x != 0))  # First letter of LHS1 cannot be 0
        problem.constraints.append(UnaryConstraint(RHS[0], lambda x: x != 0))    # First letter of RHS cannot be 0
        # Carrier variable C0 must be 0
        problem.constraints.append(UnaryConstraint('C0', lambda x: x == 0))
        # Binary Constraints
        # no there two leters map to the same value        
        for i in range(len(all_letters)):
            for j in range(i + 1, len(all_letters)):
                var1 = all_letters[i]
                var2 = all_letters[j]
                problem.constraints.append(
                    BinaryConstraint((var1, var2), lambda x, y: x != y)
                )
        # ADDITION CONSTRAINTS
        # Prepare the columns by padding with spaces on the left
        def pad(word, length):
            return [None]*(length - len(word)) + list(word)
        L0 = pad(LHS0, max_columns)
        L1 =pad(LHS1, max_columns)
        R  = pad(RHS, max_columns+1) 
        # handle the constraints of about the length
        for i in range(1, max_columns+1):
            a = L0[-i]  
            b = L1[-i]
            r = R[-i]
            cin  = carry_vars[i-1]
            cout = carry_vars[i]

            # Create auxiliary variable: stores (A,B,Cin)
            var = f"COL_{i}"
            problem.variables.append(var)
            # create domain
            problem.domains[var] = set()
            # combination of a,b,c 
            for A in (range(10) if a is not None else [0]):
                for B in (range(10) if b is not None else [0]):
                    for C in range(2):
                        problem.domains[var].add((A,B,C))
            if a is not None:
                problem.constraints.append(
                    BinaryConstraint((var, a), lambda t, x: t[0] == x)
                )
            if b is not None:
                problem.constraints.append(
                    BinaryConstraint((var, b), lambda t, x: t[1] == x)
                )
            problem.constraints.append(
                BinaryConstraint((var, cin), lambda t, x: t[2] == x)
            )
            # Constraint: (A + B + Cin) % 10 == R and (A + B + Cin) // 10 == Cout
            problem.constraints.append(
                BinaryConstraint((var, r),
                    lambda t, res: (t[0] + t[1] + t[2]) % 10 == res)
            )

            problem.constraints.append(
                BinaryConstraint((var, cout),
                    lambda t, c_out: (t[0] + t[1] + t[2]) // 10 == c_out)
            )
        # if RHS == max columns this means the last carry =0
        if len(RHS) == max_columns:
            problem.constraints.append(UnaryConstraint(carry_vars[-1], lambda x: x == 0))
        # if RHS >max columns this means the last  digit of RHS = last cary and both of them =1
        if len(RHS) > max_columns:
            problem.constraints.append(
                BinaryConstraint((RHS[0], carry_vars[max_columns]), lambda r, c: r == c)
            )
            problem.constraints.append(UnaryConstraint(RHS[0],lambda x:x==1))
            problem.constraints.append(UnaryConstraint(carry_vars[max_columns],lambda x:x==1))
        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())