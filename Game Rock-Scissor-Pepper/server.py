''' Muat library yang diperlukan
Library socket untuk menghandle koneksi antar client - server via TCP, dan
Library Thread untuk memisah proses jadi beberapa thread, di konteks ini, proses bakal diubah jadi dua thread.
Kenapa perlu dua thread ? karena untuk proses listening di sisi server, harus dipisah, satu proses untuk listening koneksi baru,
satunya lagi untuk memproses request yang udah masuk.

Library random untuk ngambil nilai random
'''
import socket
from threading import Thread
import random

# Inisiasi socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bentuk koneksi server untuk mendengarkan port di ip tertentu
# dalam konteks ini, kenapa hanya '' ? karena server mendengarkan di localhost
# hasilnya bakal sama misal diganti jadi 127.0.0.1 (seperti di client)
# untuk port, bebas diganti, selama port client sama server sama
sock.bind(('', 69))

# Minta socket untuk listening request
sock.listen()

# Tempat matching bakal didaftaring
matching_pool = []

# Tempat action (pilihan dari batu gunting kertas) user untuk didaftaring
actList = []

# Counter, gunanya untuk memisah bagian matching pool, dan mempermudah matchmaking
counter = -1

def client_handler(conn, userId, counter):

	# Beritahu fungsi supaya make variabel matching_pool secara global
	# kalo ga make ini, kemungkinan nilai dari matching_pool global ga berubah
	global matching_pool

	# Definisikan opponentIndex sejak awal, biar lebih mudah nanti pas pengecekan
	opponentIndex = None

	# Infinity loop, kaya yang dijelasin dibawah
	while True:

		# Cek, apakah user udah ada di matching pool ?
		# kalo belum ada, daftarkan user ke matching pool
		if userId not in matching_pool:
			matching_pool.append(userId)

		# Definisikan index dari user di matching pool, ini berguna, supaya kita bisa ngambil action yang tepat di actList
		# Karena konsep actList itu begini:
		# kalo ada user di index 1, maka action nya bakal di simpan di actList di index 1
		userIndex = matching_pool.index(userId)

		if len(actList) > counter * 2 + 1:

			# Cek apakah action dari user udah didaftarkan
			# kalo belum, lakukan listening ke client
			if actList[userIndex] == 0:
				actList[userIndex] = conn.recv(10).decode()

				# Kalau koneksi terputus client, maka server akan mengambil pilihan acak
				if not actList[userIndex]:
					actList[userIndex] = str(random.randint(1, 3))

			# Kalo action kita dan lawan udah ditentukan, kita lakukan pengecekan siapa yang menang
			elif actList[opponentIndex] != 0:

				if actList[opponentIndex] == "1" and actList[userIndex] == "2":
					conn.send("Rock".encode())
					conn.send("You Win".encode())
				elif actList[opponentIndex] == "2" and actList[userIndex] == "3":
					conn.send("Paper".encode())
					conn.send("You Win".encode())
				elif actList[opponentIndex] == "3" and actList[userIndex] == "1":
					conn.send("Scissor".encode())
					conn.send("You Win".encode())
				elif actList[opponentIndex] == "1" and actList[userIndex] == "3":
					conn.send("Scissor".encode())
					conn.send("You Lose".encode())
				elif actList[opponentIndex] == "2" and actList[userIndex] == "1":
					conn.send("Paper".encode())
					conn.send("You Lose".encode())
				elif actList[opponentIndex] == "3" and actList[userIndex] == "2":
					conn.send("Rock".encode())
					conn.send("You Lose".encode())
				elif actList[opponentIndex] == "1" and actList[userIndex] == "1":
					conn.send("Rock".encode())
					conn.send("The Match is Draw".encode())
				elif actList[opponentIndex] == "2" and actList[userIndex] == "2":
					conn.send("Paper".encode())
					conn.send("The Match is Draw".encode())
				elif actList[opponentIndex] == "3" and actList[userIndex] == "3":
					conn.send("Scissor".encode())
					conn.send("The Match is Draw".encode())
				else:
					conn.send("Something unexpected".encode())
					conn.send("The Match is Terminated".encode())
				break

		# Ini awal dari proses sebenarnya, yang diatas belum bakal jalan sebelum ini dieksekusi
		# Cek apakah lawannya udah ditemukan
		# Kalo lawannya belum ketemu, kita tunggu sampe ketemu
		elif opponentIndex == None:

			# Kalo misalkan jumlah matching pool ganjil, kita tunggu
			# Misal, dalam matching pool ada 3 orang, maka 2 bakal jalan, dan 1 bakal nunggu
			if len(matching_pool) % 2 == 1:
				continue

			# Cek berapa index dari lawan
			if userIndex % 2 == 0:
				opponentIndex = userIndex + 1
			else:
				opponentIndex = userIndex - 1
			
			opponent = matching_pool[opponentIndex]

			# Kirim info nama lawan ke user
			print(userIndex)
			print(matching_pool)
			conn.send(opponent.encode())

			# Daftarkan action lawan
			# Default 0
			# Ini bakal di proses di looping selanjutnya
			actList.append(0)


# Print judul
print("Server Running....")

# Infinity loop, jadi program gabakal berenti sampe dimatikan manual
while True:

	# Terima request dari client kalau ada yang masuk, dan simpan sebagai variabel conn dan addr.
	# conn itu berupa koneksi client
	# addr itu alamat dari client.
	# disini conn, bakal dipake untuk interaksi ke client,
	# dan addr untuk inisiasi identitas client
	conn, addr = sock.accept()

	# Naikkan jumlah counter, supaya proses pemisahan matching bisa jalan
	counter += 1

	# Definisikan user id supaya mudah dibaca. Bawaan dari variabel addr itu array, jadi di konversi dulu ke string
	userId = addr[0] + ":" + str(addr[1])

	# Logging untu ngecek user yang masuk matchmaking
	print(userId, "Enter the matchmaking")

	# Inisiasi thread
	# parameter target itu merupakan fungsi yang menghandle thread, jadi, semua proses yang dibagi bakal di ambil alih sama
	# fungsi bernama client_handler
	# dan parameter args itu merupakan argumen untuk fungsinya
	t = Thread(target = client_handler, args = (conn, userId, counter // 2))

	# Jalankan thread nya
	t.start()