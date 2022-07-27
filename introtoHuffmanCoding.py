import heapq, os

class BinaryTreeNode:
	def __init__(self, value, freq):
		self.value = value
		self.freq = freq 
		self.left = None
		self.right = None

	def __lt__(self, other):
		return self.freq < other.freq

	def __eq__(self, other):
		return self.freq == other.freq

class HuffmanCoding:
	def __init__(self, path):
		self.path = path
		self.__heap = []
		self.__codes = {}
		self.__reversecodes = {}
	def __make_frequency_map(self, text):
		Hashmap = {}
		for x in text:
			Hashmap[x] = Hashmap.get(x, 0) + 1

		return Hashmap

	def __buildheap(self, hashmap):
		for key in hashmap:
			frequency = hashmap[key]
			binary_tree_node = BinaryTreeNode(key, frequency)
			heapq.heappush(self.__heap, binary_tree_node)


	def __buildtree(self):
		while len(self.__heap) > 1:
			node1 = heapq.heappop(self.__heap)
			node2 = heapq.heappop(self.__heap)
			newfreq = node1.freq + node2.freq
			newnode = BinaryTreeNode(None, newfreq)
			newnode.left = node1
			newnode.right = node2
			heapq.heappush(self.__heap, newnode)

		return 

	def __buildcodesHelper(self, root, curr_bits):
		if root == None:
			return

		if root.value != None:
			self.__codes[root.value] = curr_bits
			self.__reversecodes[curr_bits] = root.value
			return

		self.__buildcodesHelper(root.left, curr_bits+'0')
		self.__buildcodesHelper(root.right, curr_bits+'1')

	def __buildcodes(self):
		root = self.__heap.pop()
		self.__buildcodesHelper(root, '')

	def __getEncodedText(self, text):
		encoded_text = ""
		for x in text:
			encoded_text += self.__codes[x]

		return encoded_text

	def __getPaddedEncodedtext(self, encoded_text):

		padded_amount = 8-len(encoded_text)%8
		for i in range(padded_amount):
			encoded_text += '0'

		padded_info = "{0:08b}".format(padded_amount)
		padded_encoded_text = padded_info + encoded_text
		return padded_encoded_text

	def __getbytesarray(self, padded_encoded_text):
		bytes_array = []
		for i in range(0,len(padded_encoded_text),8):
			byte = padded_encoded_text[i:(i+8)]
			bytes_array.append(int(byte, 2))

		return bytes_array

	def compress(self):
		file_name, file_extension = os.path.splitext(self.path)
		output_path = file_name + ".bin"
		
		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()
			text = text.rstrip()
			freq_dict = self.__make_frequency_map(text)
			self.__buildheap(freq_dict)
			self.__buildtree()
			self.__buildcodes()
			encoded_text = self.__getEncodedText(text)
			padded_encoded_text = self.__getPaddedEncodedtext

			bytes_array = self.__getbytesarray(padded_encoded_text)

			final_bytes = bytes(bytes_array)
			output.write(final_bytes)

		return output_path

	def __removePadding(self, bit_string):
		padded_info = bit_string[:8]
		extra_padding = int(padded_info, 2)

		text = bit_string[:8]
		text_after_removing_padding = text[:(-extra_padding)]
		return text_after_removing_padding

	def __decodeText(self, actual_text):
		decoded_text = ""
		current_bits = ""

		for bit in actual_text:
			current_bits += bit
			if current_bits in self.__reversecodes.keys():
				character = self.__reversecodes[current_bits]
				decoded_text += character
				current_bits = ""

		return decoded_text

	def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename = "_decompressed" + +'.txt'
		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""
			byte = file.read(1)
			while byte:
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits 
				byte = file.read(1)


			actual_text = self.__removePadding(bit_string)
			decompressed_text = self.__decodeText(actual_text)
			output.write(decompressed_text)

		return

path = str(input())
h = HuffmanCoding(path)
output_path = h.compress()
h.decompress(output_path)