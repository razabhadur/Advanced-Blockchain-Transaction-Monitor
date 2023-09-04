from web3 import Web3
import time

class AdvancedBlockchainTransactionMonitor:

    def __init__(self, network_url):
        self.web3 = Web3(Web3.HTTPProvider(network_url))
        self.last_block = self.web3.eth.blockNumber
        self.known_scam_addresses = set()
        self.address_watchlist = set()
        self.large_transfer_threshold = 10**18
        self.rapid_transaction_threshold = 5
        self.rapid_transaction_timeframe = 60

    def fetch_recent_transactions(self, num_blocks=10):
        current_block = self.web3.eth.blockNumber
        transactions = []
        for block_num in range(current_block - num_blocks + 1, current_block + 1):
            block = self.web3.eth.getBlock(block_num, full_transactions=True)
            transactions.extend(block.transactions)
        self.last_block = current_block
        return transactions

    def analyze_transactions(self, transactions):
        suspicious_txs = []
        address_activity = {}

        for tx in transactions:
            if tx['value'] > self.large_transfer_threshold:
                suspicious_txs.append((tx, 'Large transfer'))
            if tx['to'] in self.known_scam_addresses:
                suspicious_txs.append((tx, 'Transaction to known scam address'))
            if tx['to'] in self.address_watchlist or tx['from'] in self.address_watchlist:
                suspicious_txs.append((tx, 'Transaction involving watchlisted address'))
            address_activity[tx['from']] = address_activity.get(tx['from'], 0) + 1

        for address, count in address_activity.items():
            if count >= self.rapid_transaction_threshold:
                suspicious_txs.append((None, f'Rapid transactions detected from address: {address}'))

        return suspicious_txs

    def run(self):
        while True:
            transactions = self.fetch_recent_transactions()
            suspicious_txs = self.analyze_transactions(transactions)
            for tx, reason in suspicious_txs:
                if tx:
                    print(f'Suspicious transaction detected! Hash: {tx.hash.hex()}, Reason: {reason}')
                else:
                    print(reason)
            time.sleep(self.rapid_transaction_timeframe)

if __name__ == '__main__':
    network_url = input('Enter the blockchain network URL: ')
    monitor = AdvancedBlockchainTransactionMonitor(network_url)
    monitor.run()
