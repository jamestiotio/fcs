#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 5 Modular Arithmetics
# Year 2021
# James Raphael Tiovalen / 1004555

import copy
from itertools import zip_longest
from prettytable import PrettyTable


# Possible performance improvement would be to use a SageMath and/or NumPy-based implementation
class Polynomial2:
    def __init__(self, coeffs):
        self._coeffs = copy.deepcopy(coeffs)

    def __str__(self):
        result = ""

        if self._coeffs == [0] or not self._coeffs:
            return "0"

        for index, coeff in enumerate(self._coeffs[::-1]):
            if coeff == 1:
                if index == len(self._coeffs) - 1:
                    result += "1"
                else:
                    result += f"x^{len(self._coeffs) - index - 1}+"

        return result.rstrip("+")

    def __eq__(self, p2):
        return str(self) == str(p2)

    @property
    def deg(self):
        return len(self._coeffs) - 1

    @property
    def lc(self):
        return self._coeffs[-1]

    # Bit-shift right (add 0s to LSB side)
    def shift_right(self, offset):
        return Polynomial2([0] * offset + self._coeffs)

    def modulo(self, modp):
        # Check if MSB's degree qualifies
        if len(self._coeffs) >= len(modp._coeffs):
            return Polynomial2(self._coeffs[:-1]).add(Polynomial2(modp._coeffs[:-1]))

        return self

    def getInt(p):
        return int(sum(val * (2 ** idx) for idx, val in enumerate(p._coeffs)))

    def add(self, p2):
        new_coeffs = []

        for x, y in zip_longest(self._coeffs, p2._coeffs, fillvalue=0):
            new_coeffs.append(x ^ y)

        # Remove any trailing zeroes for higher order bits
        while len(new_coeffs) > 1 and new_coeffs[-1] == 0:
            new_coeffs.pop(-1)

        return Polynomial2(new_coeffs)

    def sub(self, p2):
        return self.add(p2)

    # Possible improvement:
    # - https://hal.archives-ouvertes.fr/hal-02070816/document
    # - https://hal.archives-ouvertes.fr/hal-01022757v2/document
    # Other algorithms to explore include, but are not limited to:
    # - Fast Fourier Transform
    # - Convolution in time domain
    # Both algorithms are conveniently available in NumPy as well.
    def mul(self, p2, modp=None):
        result = Polynomial2([0])

        # Iterate the multiplier to get the final product by using the long multiplication method
        for index, coeff in enumerate(p2._coeffs):
            if coeff == 1:
                result = result.add(self.shift_right(index))

        # If modp is provided, divide to obtain remainder
        if modp is not None:
            _, result = result.div(modp)

        return result

    def div(self, p2):
        q = Polynomial2([0])
        r = copy.deepcopy(self)

        b = p2
        d = b.deg
        c = b.lc

        # Perform Euclidean Division Algorithm (long division)
        while r.deg >= d:
            if r.deg == 0 and r.lc == 0:
                break
            s = Polynomial2([0 for i in range(r.deg - d)] + [1])
            q = s.add(q)
            r = r.sub(s.mul(b))

        return q, r


class GF2N:
    affinemat = [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1],
    ]

    def __init__(self, x, n=8, ip=Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])):
        self.x = x
        self.n = n
        self.ip = ip

    def __str__(self):
        return str(self.p.getInt())

    @property
    def p(self):
        return self.getPolynomial2()

    def getPolynomial2(self):
        coeffs = list(str(bin(self.x)).lstrip("0b"))
        polynomial2 = Polynomial2([int(x) for x in coeffs][::-1])
        return polynomial2

    def getInt(self):
        return self.p.getInt()

    def add(self, g2):
        # Polynomial addition, followed by reduction with respect to ip
        result = self.p.add(g2.p)
        result = result.modulo(self.ip)

        return GF2N(result.getInt(), self.n, self.ip)

    def sub(self, g2):
        return self.add(g2)

    def mul(self, g2):
        # Polynomial multiplication modulo ip
        result = self.p.mul(g2.p, self.ip)

        return GF2N(result.getInt(), self.n, self.ip)

    def div(self, g2):
        # Polynomial division
        q, r = self.p.div(g2.p)
        return GF2N(q.getInt(), self.n, self.ip), GF2N(r.getInt(), self.n, self.ip)

    def mulInv(self):
        r1, r2 = self.ip, self.p
        t1, t2 = Polynomial2([0]), Polynomial2([1])

        # Perform Extended Euclidean Algorithm
        while r2.getInt() > 0:
            q, r = r1.div(r2)
            r1 = Polynomial2(copy.deepcopy(r2._coeffs))
            r2 = r
            t = t1.sub(q.mul(t2, self.ip))
            t1 = Polynomial2(copy.deepcopy(t2._coeffs))
            t2 = t

        return GF2N(t1.getInt(), self.n, self.ip)

    def affineMap(self):
        # Fill up 0s in p1 for more significant bits for matrix multiplication
        p1_coeffs = copy.deepcopy(self.p._coeffs)
        for i in range(len(p1_coeffs), 8):
            p1_coeffs.append(0)
        temp_coeffs = []
        for i in range(8):
            sum = 0
            for j in range(8):
                sum += p1_coeffs[j] * self.affinemat[i][j]
            temp_coeffs.append(sum % 2)
        p3 = Polynomial2(temp_coeffs).add(Polynomial2([1, 1, 0, 0, 0, 1, 1, 0]))
        return GF2N(p3.getInt(), self.n, self.ip)


if __name__ == "__main__":
    print("\nTest 1")
    print("======")
    print("p1 = x^5+x^2+x")
    print("p2 = x^3+x^2+1")
    p1 = Polynomial2([0, 1, 1, 0, 0, 1])
    p2 = Polynomial2([1, 0, 1, 1])
    p3 = p1.add(p2)
    print("p3 = p1 + p2 =", p3)
    assert p3 == Polynomial2([1, 1, 0, 1, 0, 1])

    print("\nTest 2")
    print("======")
    print("p4 = x^7+x^4+x^3+x^2+x")
    print("modp = x^8+x^7+x^5+x^4+1")
    p4 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
    # modp = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    modp = Polynomial2([1, 0, 0, 0, 1, 1, 0, 1, 1])
    p5 = p1.mul(p4, modp)
    print("p5 = p1 * p4 mod (modp) =", p5)
    assert p5 == Polynomial2([0, 0, 0, 1, 1, 0, 1, 1])

    print("\nTest 3")
    print("======")
    print("p6 = x^12+x^7+x^2")
    print("p7 = x^8+x^4+x^3+x+1")
    p6 = Polynomial2([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    p7 = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    p8q, p8r = p6.div(p7)
    print("q for p6 / p7 =", p8q)
    print("r for p6 / p7 =", p8r)
    assert p8q == Polynomial2([1, 0, 0, 0, 1]) and p8r == Polynomial2(
        [1, 1, 1, 1, 0, 1]
    )

    ####
    print("\nTest 4")
    print("======")
    g1 = GF2N(100)
    g2 = GF2N(5)
    print("g1 =", g1.getPolynomial2())
    print("g2 =", g2.getPolynomial2())
    g3 = g1.add(g2)
    print("g1 + g2 =", g3.p)
    assert g3.p == Polynomial2([1, 0, 0, 0, 0, 1, 1])

    print("\nTest 5")
    print("======")
    ip = Polynomial2([1, 1, 0, 0, 1])
    print("irreducible polynomial", ip)
    g4 = GF2N(0b1101, 4, ip)
    g5 = GF2N(0b110, 4, ip)
    print("g4 =", g4.getPolynomial2())
    print("g5 =", g5.getPolynomial2())
    g6 = g4.mul(g5)
    print("g4 x g5 =", g6.p)
    assert g6.p == Polynomial2([0, 0, 0, 1])

    print("\nTest 6")
    print("======")
    g7 = GF2N(0b1000010000100, 13, None)
    g8 = GF2N(0b100011011, 13, None)
    print("g7 =", g7.getPolynomial2())
    print("g8 =", g8.getPolynomial2())
    q, r = g7.div(g8)
    print("g7 / g8 =")
    print("q =", q.getPolynomial2())
    print("r =", r.getPolynomial2())
    assert q.p == Polynomial2([1, 0, 0, 0, 1]) and r.p == Polynomial2(
        [1, 1, 1, 1, 0, 1]
    )

    print("\nTest 7")
    print("======")
    ip = Polynomial2([1, 1, 0, 0, 1])
    print("irreducible polynomial", ip)
    g9 = GF2N(0b101, 4, ip)
    print("g9 =", g9.getPolynomial2())
    print("inverse of g9 =", g9.mulInv().getPolynomial2())
    assert g9.mulInv().p == Polynomial2([1, 1, 0, 1])

    print("\nTest 8")
    print("======")
    ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
    print("irreducible polynomial", ip)
    g10 = GF2N(0xC2, 8, ip)
    print("g10 = 0xc2")
    g11 = g10.mulInv()
    print("inverse of g10 = g11 =", hex(g11.getInt()))
    g12 = g11.affineMap()
    print("affine map of g11 =", hex(g12.getInt()))
    assert g11.p == Polynomial2([1, 1, 1, 1, 0, 1]) and g12.p == Polynomial2(
        [1, 0, 1, 0, 0, 1, 0, 0]
    )

    # Generate table for addition for GF(2^4)
    print("\nWriting addition table for GF(2^4) to table1.txt file...")
    base_ls = []
    for i in range(16):
        base_ls.append(GF2N(i))
    table_rows = []
    for row_base in base_ls:
        row = []
        for col_base in base_ls:
            row.append(row_base.add(col_base))
        table_rows.append(row)
    base_ls = [str(base_val.p) for base_val in base_ls]
    headers = ["GF(2^4) +"] + base_ls
    addition_table = PrettyTable(headers)
    addition_table.align = "c"
    for i, val in enumerate(base_ls):
        row = table_rows[i]
        row = ["{:02}".format(cell_val.getInt()) for cell_val in row]
        addition_table.add_row([val] + row)
    with open("table1.txt", "w") as file:
        file.write(addition_table.get_string())

    with open("table1.txt", "a") as file:
        file.write("\n\n")

    # Generate table for multiplication for GF(2^4)
    print("\nWriting multiplication table for GF(2^4) to table1.txt file...")
    ip = Polynomial2([1, 0, 0, 1, 1])
    base_ls = []
    for i in range(16):
        base_ls.append(GF2N(i, 4, ip))
    table_rows = []
    for row_base in base_ls:
        row = []
        for col_base in base_ls:
            row.append(row_base.mul(col_base))
        table_rows.append(row)
    base_ls = [str(base_val.p) for base_val in base_ls]
    headers = ["GF(2^4) *"] + base_ls
    multiplication_table = PrettyTable(headers)
    multiplication_table.align = "c"
    for i, val in enumerate(base_ls):
        row = table_rows[i]
        row = ["{:02}".format(cell_val.getInt()) for cell_val in row]
        multiplication_table.add_row([val] + row)
    with open("table1.txt", "a") as file:
        file.write(multiplication_table.get_string())

    # Generate table for AES S-Box
    print("\nWriting table for AES S-Box to table2.txt file...")
    headers = ["AES S-Box"]
    for i in range(16):
        headers.append("{:02x}".format(i))
    aes_sbox_table = PrettyTable(headers)
    for j in range(16):
        row = ["{:x}0".format(j)]
        for k in range(16):
            inp = (j << 4) + k
            out = GF2N(inp).mulInv().affineMap().getInt()
            row.append("{:02x}".format(out))
        aes_sbox_table.add_row(row)
    with open("table2.txt", "w") as file:
        file.write(str(aes_sbox_table))
