#Where logic is handled. duh



class NumbleGame:
    def __init__(self, solution):
        if not (solution.isdigit() and len(solution) == 5):
            raise ValueError("5 digit number only")
        self.solution = solution
        self.guess_made = False
        self.last_feedback = []

    def submit_guess(self, guess):
        if self.guess_made:
            raise Exception("one guess allowed.")
        if not (guess.isdigit() and len(guess) == 5):
            raise ValueError("must be  5 digit number.")

        self.guess_made = True
        self.last_feedback = self._check_guess(guess)
        return self.last_feedback

    def _check_guess(self, guess):
        feedback = ["absent"] * 5
        solution_digits = list(self.solution)
        guess_digits = list(guess)

        # First pass: correct digits in correct place
        for i in range(5):
            if guess_digits[i] == solution_digits[i]:
                feedback[i] = "correct"
                solution_digits[i] = None
                guess_digits[i] = None

        # Second pass: correct digits in wrong place
        for i in range(5):
            if guess_digits[i] and guess_digits[i] in solution_digits:
                feedback[i] = "misplaced"
                solution_digits[solution_digits.index(guess_digits[i])] = None

        return feedback
