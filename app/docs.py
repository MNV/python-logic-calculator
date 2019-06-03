class Docs:
    def __init__(self):
        """Class constructor"""
        self.doc = """
***************************************************
***  Welcome to Mathematical logic calculator!  ***
***************************************************

Please, read the instruction carefully before using the program.
Allowed operators to use:
        Conjunction (AND): and
        Disjunction (OR): or
        Inversion (NOT): not
        Implication (IF...THEN): implies
        Equivalence (EQUALS TO): ==
        Exclusive or (XOR): xor
        Peirce arrow (OR-NOT): nor
        Sheffer stroke (AND-NOT): nand
        Round brackets: ()
        Letters: xyz
        Numbers: 01
Examples:
        1. implies(nor(x,y), nand(y,z))
        2. nand(x,y) or nor(x,z)
        3. implies(nand(x,y), nand(x,z))
        4. implies(not(x or y), nand(y,z))
        5. xor(xor(1, x and y), x and z)
        6. (implies(nand(x, y), nor(y, z))) or not(implies(not(x), not(z)))
        7. implies(x, z) == implies(y, not(z))
        8. xor(implies(x, z), implies(y, not(z)))
        9. implies(x and z, z or y)
        10. x or y and x or y
        """

    def get_welcome_message(self) -> str:
        """Returns documentation string"""
        return self.doc
