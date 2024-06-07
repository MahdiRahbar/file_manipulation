import os



def chop_file(file_path, output_path='', chop_size = 1500): 
def chop_file(file_path, output_path='', chunk_size = 1500): 
    chunk_size = chunk_size * 10**6
    file_size = os.path.getsize(file_path)
    q, _ = divmod(file_size, chunk_size)
    chunk_number = q + 1 
    if output_path == '':
        output_path = file_path
    
    file_content = bytes(open(file_path, 'rb').read())
    for i in range(chunk_number): 
        if i != chunk_number-1: 
            with open(output_path + f"_part{i+1}", 'wb+') as f: 
                f.write(file_content[chunk_size*i:chunk_size*(i+1)])
        else:
            with open(output_path + f"_part{i+1}", 'wb+') as f: 
                f.write(file_content[chunk_size*i:])



def rebuild_file(org_filename, dir_path='./'): 
    file_list = os.listdir(dir_path)
    chunk_list = []
    chunk_order = [] 
    
    for fname in file_list:
        if (os.path.isfile(os.path.join(dir_path,fname)) and
                org_filename in fname and \
                fname[-1].isdigit()
           ):
            chunk_list.append(fname)
            chunk_order.append(int(fname[-1]))
    sorted_chunks = [i for i,_ in sorted(zip(chunk_list, chunk_order))]
    print(sorted_chunks)
    with open(os.path.join(dir_path,f"rebuilt_{org_filename}"), 'wb') as f:
        pass
    for f in sorted_chunks: 
        with open(os.path.join(dir_path,f), 'rb') as f: 
            tmp_chunk = bytes(f.read())
        with open(os.path.join(dir_path,f"rebuilt_{org_filename}"), 'ab') as f:
            f.write(tmp_chunk)
    print("Rebuilding file is was successful!") 
            
            
import sys
import hashlib


def hashfile(file):

	# A arbitrary (but fixed) buffer 
	# size (change accordingly)
	# 65536 = 65536 bytes = 64 kilobytes 
	BUF_SIZE = 65536

	# Initializing the sha256() method
	sha256 = hashlib.sha256()

	# Opening the file provided as
	# the first commandline argument
	with open(file, 'rb') as f:
		
		while True:
			
			# reading data = BUF_SIZE from
			# the file and saving it in a
			# variable
			data = f.read(BUF_SIZE)

			# True if eof = 1
			if not data:
				break
	
			# Passing that data to that sh256 hash
			# function (updating the function with
			# that data)
			sha256.update(data)

	
	# sha256.hexdigest() hashes all the input
	# data passed to the sha256() via sha256.update()
	# Acts as a finalize method, after which
	# all the input data gets hashed hexdigest()
	# hashes the data, and returns the output
	# in hexadecimal format
	return sha256.hexdigest()


if __name__ == "__main__":
    org_filename = "model-00001-of-00002.safetensors"
    directory = "./"
    file_path = "./{org_filename}}"
    chop_file(file_path)
    rebuild_file(org_filename)

    f1_hash = hashfile(f"./{org_filename}")
    f2_hash = hashfile(f"./rebuilt_{org_filename}")

    # Doing primitive string comparison to 
    # check whether the two hashes match or not
    if f1_hash == f2_hash:
        print("Both files are same")
        print(f"Hash: {f1_hash}")
