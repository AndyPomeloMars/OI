class Maths():
    def factorial(self, n):
        res = 1
        for i in range(1, n + 1):
            res *= i
        return res
    
    def a(self, n, m):
        if not (n - m):
            return Maths.factorial(n)
        else:
            return Maths.factorial(n) // Maths.factorial(n - m)

    def c(self, n, m):
        m = min(m, n - m)
        return  Maths.a(n, m) //  Maths.a(m, m)
    
    def gcd(self, a, b):
        return a if not b else Maths.gcd(b, a % b)

    def lcm(self, a, b):
        return a * b // Maths.gcd(a, b)

    def exgcd(self, a, b):
        x,  y,  s,  t = 1, 0, 0, 1
        while b:
            q, r = divmod(a, b)
            a, b = b, r
            x, s = s, x - q * s
            y, t = t, y - q * t
        return [x, y, a]
    
    def sqrt(self, x, err = 1e-6):
        res = x
        while abs(res * res - x) > err:
            res = (res + x / res) / 2
        return res

    def fibonacci(self, n):
        if n < 2:
            return n
        x, y = Maths.fibonacci((n >> 1) - 1), Maths.fibonacci(n >> 1)
        if n & 0x1:
            x += y
            return x * x + y * y
        else:
            return y * (y + 2 * x)
    
    def is_prime(self, x):
        if not x or x == 1:
            return False
        if x == 2:
            return True
        for i in range(3, int(Maths.sqrt(x)) + 1):
            if not x % i:
                return False
        return True

    def sieve(self, n):
        cnt, st, pri = 0, [True] * (n + 1), [0] * (n + 1)
        st[0] = st[1] = False
        for i in range(2, n + 1):
            if st[i]:
                pri[cnt] = i
                cnt += 1
            for j in range(cnt):
                if pri[j] * i > n: 
                    break
                st[pri[j] * i] = False
                if not i % pri[j]: 
                    break
        return st[0:]
    
    def get_prime(self, n):
        st, pri = Maths.sieve(n), []
        for i in range(n + 1):
            if st[i]:
                pri.append(i)
        return pri
    
    def factor(self, x):
        st = Maths.sieve(x)
        faclst = []
        for i in range(2, int(Maths.sqrt(x)) + 1):
            if not st[i]:
                continue
            cnt = 0
            while not x % i:
                cnt += 1
                x /= i
            if cnt:
                faclst.append([i, cnt])
        if x > 1:
            faclst.append([x, 1])
        return faclst
    
    def catalan(self, n):
        x = y = 1
        for i in range(2, n + 1):
            x, y = (x * (n + i), y * i)
        return x // y

    def dectob(self, x, base = 2):
        convertString = "0123456789ABCDEF"
        if x < base:
            return convertString[x]
        else:
            return Maths.dectob(x // base, base) + convertString[x % base]