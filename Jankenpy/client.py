''' Muat library yang diperlukan
sebenarnya sama aja kaya yang di server, tapi disini kita make library os, supaya bisa make perintah clear( untuk bersihin cmd )
'''
import socket
import os


while True:
	print("Janken Client")
	print("1. Start matchmaking")
	print("2. Clear Screen")
	print("9. Close")

	command = input(":")

	if command == "1":
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Sebuah catatan
		# 127.0.0.1 itu ip localhost
		# dan port 69 itu port acak, bisa diubah sesuai selera
		# selama port di client sama port di server sama
		# dan untuk ip, kalau testing di satu komputer, maka ini gaperlu diganti
		# tapi kalo mau testing di beda komputer, maka harus diganti sama ip server
		# 
		sock.connect(('127.0.0.1', 69))
		print("Connection estabilished")
		print("Waiting for opponent...")
		# Tampilkan nama lawan, sebelum dikirim sama server, client bakal terus listening
		print("Match Created ! Opponent: ", sock.recv(1024).decode())
		print("Please select the option")
		print("1. Rock")
		print("2. Paper")
		print("3. Scissor")
		while True:
			act = input("Action: ")

			# Cek apakah aksi yang dikirim udah sesuai format, kalo ga sesuai, minta lagi
			if act == "1" or act == "2" or act == "3":

				# tentukan pilihan player dalam bentuk kata kata
				if act == "1":
					action = "Rock"
				elif act == "2":
					action = "Paper"
				else:
					action = "Scissor"

				# Tampilkan hasil yang dipilih oleh player
				print("You choose: ", action)

				# Kirim aksi ke server
				sock.send(act.encode())
				print("Waiting opponent to respond...")

				# Tampilkan action lawan, sebelum dikirim server, client bakal terus listening
				print("Opponent choose:", sock.recv(1024).decode())

				# Terima hasil
				print(sock.recv(1024).decode())
				print()
				break


	elif command == "2":
		# Bersihkan layar cmd
		os.system("cls")

	# Tutup aplikasi
	# Kalo nggak make angka 9, maka bakal terus looping
	elif command == "9":
		print("Thank you for playing")
		break

''' Catatan tambahan
di bagian sock.recv dan sock.send, ada bagian encode sama decode, itu maksudnya, string yang mau dikirim bakal di ubah dulu keformat
yang diterima sama tcp. Karena kalo ga diencode dulu, gabisa di kirim
'''