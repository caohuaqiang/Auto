import unittest


class MS(unittest.TestCase):
    def setUp(self):
        self.shuju = [1,8,3,5,9,0,2,4,7,6]
        self.fb = [1,6,7,13,20,33]

    @unittest.skip('跳过')
    def test_maopao(self):
        shuju = self.shuju
        # for data in shuju:
        #     if

        num = len(shuju)
        print(num)
        for i in range(num):
            for j in range(i+1):
                if shuju[i] < shuju[j]:
                    shuju[i], shuju[j] = shuju[j], shuju[i]

        print(shuju)

    @unittest.skip('跳过')
    def test_paixu(self):
        shuju = self.shuju
        A = sorted(shuju)
        print(A)

    @unittest.skip('跳过')
    def test_jihe(self):
        A = {1,3,8}
        B = {1,8,6}
        C = A.intersection(B)
        print(C)
        D = sorted(C)
        print(D)

    # @unittest.skip('跳过')
    def test_shulie(self):
        A = []
        for i in range(1000):
            if i == 0:
                A.append(1)
            elif i == 1:
                A.append(3)
            else:
                x = A[i-1] + A[i-2]
                if x >500:
                    break
                else:
                    A.append(x)

        print(A)




if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(MS("test_shulie"))
    runner = unittest.TextTestRunner()
    runner.run(suite)