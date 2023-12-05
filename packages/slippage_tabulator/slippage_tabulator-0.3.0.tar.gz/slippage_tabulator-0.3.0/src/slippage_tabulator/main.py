from uniswap_main import Uniswap
from web3 import Web3

class UniPolicies:
    def __init__(self):
        self.uni=Uniswap()
        self.web3=Web3(Web3.HTTPProvider('https://reth.shield3.com/rpc'))

    def max_slippage_is_equal_to_greater_than(self,threshold,input_data):
        max_slippage=-2**256
        slippage_data=self.uni.get_potential_slippage(self.web3,input_data)
        for key in slippage_data.keys():
            if slippage_data[key]['max_slippage']>max_slippage:
                max_slippage=slippage_data[key]['max_slippage']
                if max_slippage>=threshold:
                    return True
        return False
    
    def max_slippage_is_greater_than(self,threshold,input_data):
        max_slippage=-2**256
        slippage_data=self.uni.get_potential_slippage(self.web3,input_data)
        for key in slippage_data.keys():
            if slippage_data[key]['max_slippage']>max_slippage:
                max_slippage=slippage_data[key]['max_slippage']
                if max_slippage>threshold:
                    return True
        return False
    
    def highest_average_slippage_is_equal_to_greater_than(self,threshold,input_data):
        max_avg_slippage=-2**256
        slippage_data=self.uni.get_potential_slippage(self.web3,input_data)
        for key in slippage_data.keys():
            if slippage_data[key]['weighted_slippage']>max_avg_slippage:
                max_avg_slippage=slippage_data[key]['weighted_slippage']
                if max_avg_slippage>=threshold:
                    return True
        return False

    def highest_average_slippage_is_greater_than(self,threshold,input_data):
        max_avg_slippage=-2**256
        slippage_data=self.uni.get_potential_slippage(self.web3,input_data)
        for key in slippage_data.keys():
            if slippage_data[key]['weighted_slippage']>max_avg_slippage:
                max_avg_slippage=slippage_data[key]['weighted_slippage']
                if max_avg_slippage>threshold:
                    return True
        return False
    
# result=UniPolicies().highest_average_slippage_is_equal_to_greater_than(0.05,"0x3593564c000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000656e3c7f00000000000000000000000000000000000000000000000000000000000000020a080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000001600000000000000000000000005026f006b85729a8b14553fae6af249ad16c9aab000000000000000000000000ffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000006595c73400000000000000000000000000000000000000000000000000000000000000020000000000000000000000003fc91a3afd70395cd496c647d5a6cc9d4b2b7fad00000000000000000000000000000000000000000000000000000000656e413c00000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000000411eeb5aff68c452475d5151b1fb8093e1d1d8d9c286870ff0f58b188ab4d85034099f0960701005858efd3642ad465e8279cb50c59d045921bb79521895b9cb831c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000084595161401484a0000000000000000000000000000000000000000000000000000000f434c042a6b743f00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000005026f006b85729a8b14553fae6af249ad16c9aab000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
# print(result)