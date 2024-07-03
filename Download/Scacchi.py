import tkinter as tk
from functools import partial		

class campo_scacchi(tk.Tk):
	def __init__(self):
		super().__init__()
		#inizializzazione variabili
		self.grandezza_campo = 8
		self.quadrati_campo = []
		self.k = 0
		self.conteggio_tocchi = 0
		self.lista_colori = ["#ffce9e", "#d18b47"]
		self.pedina_da_spostare = ""
		self.old_click = 0
		self.mosse_re = []
		self.mosse_pedoni = []
		self.mosse_cavallo = []
		self.conteggio_click = 0
		self.chi_clicka = 0
		
		#torre
		self.mosse_torri_a = []
		self.mosse_torri_i = []
		self.mosse_torri_d = []
		self.mosse_torri_s = []
		
		#alfieri
		self.mosse_alfieri_ad = []
		self.mosse_alfieri_as = []
		self.mosse_alfieri_bd = []
		self.mosse_alfieri_bs = []
		
		#regina
		self.mosse_queen_dad = []
		self.mosse_queen_das = []
		self.mosse_queen_dbd = []
		self.mosse_queen_dbs = []
		
		self.mosse_queen_ra = []
		self.mosse_quuen_ri = []
		self.mosse_quuen_rd = []
		self.mosse_quuen_rs = []
		
		self.geometry("705x713")
		self.resizable(0, 0)
		self.title("Alba - Scacchi")
		self.crea_widgets()
	
	def crea_widgets(self):
		self.contenitore_campo = tk.Frame(self)
		self.contenitore_campo.grid()
		
		self.disegna_campo()	
		self.posiziona_pedine()
		self.black_dont_play()
		
	def disegna_campo(self):
		for i in range(self.grandezza_campo):
			#colorazione tastiera
			if i == 1 or i == 3 or i == 5 or i == 7:
				self.lista_colori = []
				self.lista_colori.extend(["#d18b47", "#ffce9e"])
			else:
				self.lista_colori = []
				self.lista_colori.extend(["#ffce9e", "#d18b47"])
				
			for j in range(self.grandezza_campo):
				if self.k == 2:
					self.k = 0
					
				cmp_btn = tk.Button(self.contenitore_campo, bg = self.lista_colori[self.k], width = 5, height = 3, font = ("Arial", 16), fg = "yellow", command = partial(self.mossa, i, j))
				cmp_btn.grid(row = i, column = j)
				self.quadrati_campo.append(cmp_btn)
				self.k += 1
	
	def colora_quadrati(self):
		k = 0
		i = 0
		
		for widget in self.contenitore_campo.winfo_children():
			if i > 7 and i <= 15 or i > 23 and i <= 31 or i > 39 and i <= 47 or i > 55 and i <= 63:
				self.lista_colori = []
				self.lista_colori.extend(["#d18b47", "#ffce9e"])
			else:
				self.lista_colori = []
				self.lista_colori.extend(["#ffce9e", "#d18b47"])
				
			if k == 2:
				k = 0
				
			widget.config(bg = self.lista_colori[k])
			i += 1
			k += 1
		
				
	def posiziona_pedine(self):
		i = 0
		y = 0
		
		lista_pedine_avversari = ["♜", "♝", "♞", "♛", "♚", "♞", "♝", "♜", "♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"]
		lista_pedine_amico = ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟", "♜", "♝", "♞", "♛", "♚", "♞", "♝", "♜"]
		
		for quad in self.quadrati_campo:
			if i <= 15:
				quad["fg"] = "black"
				quad["text"] = lista_pedine_avversari[i]
			
			if i >= 48:
				quad["fg"] = "white"
				quad["text"] = lista_pedine_amico[y]
				y += 1
				
			i += 1
		
	def mossa(self, riga, colonna):
		clicked = (riga * 8) + colonna
		self.abilita_celle_turno(clicked)
		
		#controllo giocata
		if self.quadrati_campo[clicked]["bg"] == "gray":
			self.quadrati_campo[self.old_click]["text"] = ""
			self.quadrati_campo[self.old_click]["fg"] = "yellow"
			self.quadrati_campo[clicked]["text"] = self.pedina_da_spostare
			self.conteggio_tocchi += 1
			self.conteggio_click = -1
			
			self.who_play(clicked)
			self.colora_quadrati()

		else:	
			#mossa pedoni
			if self.quadrati_campo[clicked]["text"] == "♟":
				self.colora_quadrati()
				self.cambia_posto("♟", clicked)				
				self.check_play_pedon(clicked, riga, colonna)
				
				for h in self.mosse_pedoni:
					self.quadrati_campo[h]["bg"] = "gray"
				
				self.check_if_pedon_can_eat(clicked, riga, colonna)
			
			#mossa re
			if self.quadrati_campo[clicked]["text"] == "♚":
				self.colora_quadrati()
				self.cambia_posto("♚", clicked)
				self.check_play_king(riga, colonna)
						
				for h in self.mosse_re:
					if self.quadrati_campo[h] != self.quadrati_campo[clicked]:
						self.quadrati_campo[h]["bg"] = "gray"
				
				self.check_if_king_can_eat(clicked)
			
			#mosse torri
			if self.quadrati_campo[clicked]["text"] == "♜":
				self.colora_quadrati()
				self.cambia_posto("♜", clicked)
				self.check_play_tower(clicked, riga, colonna)
				mosse_t = [self.mosse_torri_a, self.mosse_torri_i, self.mosse_torri_d, self.mosse_torri_s]
				
				for i in range(4):
					for h in mosse_t[i]:
						if self.quadrati_campo[h] != self.quadrati_campo[clicked]:
							self.quadrati_campo[h]["bg"] = "gray"
							self.quadrati_campo[h]["state"] = "normal"
					
				self.check_if_tower_can_eat(clicked)
			
			#mosse cavallo
			if self.quadrati_campo[clicked]["text"] == "♞":
				self.colora_quadrati()
				self.cambia_posto("♞", clicked)
				self.check_play_horse(clicked, riga, colonna)
				
				for h in self.mosse_cavallo:
					if self.quadrati_campo[h] != self.quadrati_campo[clicked]:
						self.quadrati_campo[h]["bg"] = "gray"
				
				self.check_if_horse_can_eat(clicked)
			
			#mosse alfiere
			if self.quadrati_campo[clicked]["text"] == "♝":
				self.colora_quadrati()
				self.cambia_posto("♝", clicked)
				self.check_play_bishop(clicked, riga, colonna)
				mosse_a = [self.mosse_alfieri_ad, self.mosse_alfieri_as, self.mosse_alfieri_bd, self.mosse_alfieri_bs]
				
				for i in range(4):
					for h in mosse_a[i]:
						if self.quadrati_campo[h] != self.quadrati_campo[clicked]:
							self.quadrati_campo[h]["bg"] = "gray"
							self.quadrati_campo[h]["state"] = "normal"
				
				self.check_if_bishop_can_eat(clicked)
			
			#mosse regina
			if self.quadrati_campo[clicked]["text"] == "♛":
				self.colora_quadrati()
				self.cambia_posto("♛", clicked)
				self.check_play_queen(clicked, riga, colonna)
				mosse_o = [self.mosse_queen_ra, self.mosse_quuen_ri, self.mosse_quuen_rd, self.mosse_quuen_rs]
				mosse_d = [self.mosse_queen_dad,  self.mosse_queen_das, self.mosse_queen_dbd, self.mosse_queen_dbs]
				
				for i in range(4):
					for h in mosse_o[i]:
						if self.quadrati_campo[h] != self.quadrati_campo[clicked]:
							self.quadrati_campo[h]["bg"] = "gray"
							self.quadrati_campo[h]["state"] = "normal"
				
				for i in range(4):
					for h in mosse_d[i]:
						if self.quadrati_campo[h] != self.quadrati_campo[clicked]:
							self.quadrati_campo[h]["bg"] = "gray"
							self.quadrati_campo[h]["state"] = "normal"
				
				self.check_if_queen_can_eat(clicked)
			
		self.conteggio_click += 1
		if self.conteggio_click == 1:
			self.chi_clicka = clicked
		
		if self.chi_clicka == clicked:
			if self.conteggio_click == 2:
				self.colora_quadrati()
				self.abilita_celle(clicked)
				self.conteggio_click = 0
		else:
			self.conteggio_click = 0
		
		if self.conteggio_click == 1:
			self.chi_clicka = clicked
	
	def abilita_celle(self, clicked):
		if self.quadrati_campo[clicked]["fg"] == "white":
			amico = "white"
		elif self.quadrati_campo[clicked]["fg"] == "black":
			amico = "black"
			
		for ped in self.contenitore_campo.winfo_children():
			if ped["fg"] == amico:
				ped.configure(state = "normal")
		
	def cambia_posto(self, pedone, posizione):
		self.pedina_da_spostare = pedone
		self.old_click = posizione
	
	def who_play(self, cliccato):	
		if self.conteggio_tocchi % 2 == 0:
			self.quadrati_campo[cliccato]["fg"] = "black"
			
			for ped in self.contenitore_campo.winfo_children():
				if ped["fg"] == "black":
					ped.configure(state = "disable")
			
			for ped in self.contenitore_campo.winfo_children():
				if ped["fg"] == "white" or ped["text"] == "":
					ped.configure(state = "normal")
			
		else:
			self.quadrati_campo[cliccato]["fg"] = "white"
			
			for ped in self.contenitore_campo.winfo_children():
				if ped["fg"] == "white":
					ped.configure(state = "disable")
			
			for ped in self.contenitore_campo.winfo_children():
				if ped["fg"] == "black" or ped["text"] == "":
					ped.configure(state = "normal")
	
	def black_dont_play(self):
		for ped in self.contenitore_campo.winfo_children():
			if ped["fg"] == "black":
				ped.configure(state = "disable")
				
	def abilita_celle_turno(self, clicked):
		if self.quadrati_campo[clicked]["fg"] == "white":
			for wg in self.contenitore_campo.winfo_children():
				if wg["fg"] == "white":
					wg["state"] = "normal"
					
				if wg["fg"] == "yellow":
					wg["state"] = "normal"
					
		elif self.quadrati_campo[clicked]["fg"] == "black":
			for wg in self.contenitore_campo.winfo_children():
				if wg["fg"] == "black":
					wg["state"] = "normal"
				
				if wg["fg"] == "yellow":
					wg["state"] = "normal"
			
	
	def check_play_pedon(self, clicked, riga, colonna):
		self.mosse_pedoni = []
		
		if self.quadrati_campo[clicked]["fg"] == "white":
			if clicked > 47:
				if riga - 1 >= 0 and riga - 1 <= 7:
					dritto_amico_di_uno = ((riga - 1) * 8) + colonna
					self.mosse_pedoni.append(dritto_amico_di_uno)
				
				if riga - 2 >= 0 and riga - 2 <= 7:
					dritto_amico_di_due = ((riga - 2) * 8) + colonna
					self.mosse_pedoni.append(dritto_amico_di_due)
				
			else:
				if riga - 1 >= 0 and riga - 1 <= 7:
					dritto_amico_di_uno = ((riga - 1) * 8) + colonna
					self.mosse_pedoni.append(dritto_amico_di_uno)
			
			if colonna + 1 >= 0 and colonna + 1 <= 7:
				diagonale_amica_destra = ((riga - 1) * 8) + colonna + 1
				
				if self.quadrati_campo[diagonale_amica_destra]["fg"] == "black":
					self.mosse_pedoni.append(diagonale_amica_destra)
			
			if colonna - 1 >= 0 and colonna - 1 <= 7:
				diagonale_amica_sinistra = ((riga - 1) * 8) + colonna - 1
				
				if self.quadrati_campo[diagonale_amica_sinistra]["fg"] == "black":
				 	self.mosse_pedoni.append(diagonale_amica_sinistra)
		else:
			if clicked < 16:
				if riga + 1 >= 0 and riga + 1 <= 7:
					dritto_nemico_di_uno = ((riga + 1) * 8) + colonna
					self.mosse_pedoni.append(dritto_nemico_di_uno)
					
				if riga + 2 >= 0 and riga + 2 <= 7:
					dritto_nemico_di_due = ((riga + 2) * 8) + colonna
					self.mosse_pedoni.append(dritto_nemico_di_due)
				
			else:
				if riga + 1 >= 0 and riga + 1 <= 7:
					dritto_nemico_di_uno = ((riga + 1) * 8) + colonna
					self.mosse_pedoni.append(dritto_nemico_di_uno)
		
			if colonna + 1 >= 0 and colonna + 1 <= 7:
				diagonale_nemica_destra = ((riga + 1) * 8) + colonna + 1
				
				if self.quadrati_campo[diagonale_nemica_destra]["fg"] == "white":
					self.mosse_pedoni.append(diagonale_nemica_destra)
			
			if colonna - 1 >= 0 and colonna - 1 <= 7:
				diagonale_nemica_sinistra = ((riga + 1) * 8) + colonna - 1
			
				if self.quadrati_campo[diagonale_nemica_sinistra]["fg"] == "white":
				 	self.mosse_pedoni.append(diagonale_nemica_sinistra)
					 
	def check_play_king(self, riga, colonna):
		self.mosse_re = []
	
		for i in range(max(0, riga-1), min(riga+2, 8)):
			for j in range(max(0, colonna-1), min(colonna+2, 8)):
				self.mosse_re.append(i * 8 + j)
	
	def check_play_tower(self, clicked, riga, colonna):
		self.mosse_torri_a = []
		self.mosse_torri_i = []
		self.mosse_torri_d = []
		self.mosse_torri_s = []
		
		#avanti
		for n in range(riga+1):
			self.mosse_torri_a.append(((riga - n) * 8) + colonna)
		
		#destra
		for c in range(8-colonna):
			self.mosse_torri_d.append(((riga) * 8) + (colonna + c))
		
		#indietro
		for n in range(8-riga):
			self.mosse_torri_i.append(((riga + n) * 8) + colonna)
		
		#sinistra
		for c in range(colonna + 1):
			self.mosse_torri_s.append(((riga) * 8) + (c))
	
	def check_play_horse(self, clicked, riga, colonna):
		self.mosse_cavallo = []
		
		if self.quadrati_campo[clicked]["fg"] == "white":
			avanti_sinistra = ((riga - 2) * 8) + (colonna - 1)
			avanti_destra = ((riga - 2) * 8) + (colonna + 1)
			
			indietro_destra = ((riga + 2) * 8) + (colonna - 1)
			indietro_sinistra =	((riga + 2) * 8) + (colonna + 1)
			
			destra_avanti = ((riga - 1) * 8) + (colonna + 2)
			destra_indietro = ((riga - 1) * 8) + (colonna - 2)
			
			sinistra_avanti = ((riga + 1) * 8) + (colonna + 2)
			sinistra_indietro = ((riga + 1) * 8) + (colonna - 2)
			
			if (riga - 2) >= 0 and (riga - 2) <= 7 and (colonna - 1) >= 0 and (colonna - 1) <= 7:
				self.mosse_cavallo.append(avanti_sinistra)
			
			if (riga - 2) >= 0 and (riga - 2) <= 7 and (colonna + 1) >= 0 and (colonna + 1) <= 7:
				self.mosse_cavallo.append(avanti_destra)
			
			if (riga + 2) >= 0 and (riga + 2) <= 7 and (colonna - 1) >= 0 and (colonna - 1) <= 7:
				self.mosse_cavallo.append(indietro_destra)
			
			if (riga + 2) >= 0 and (riga + 2) <= 7 and (colonna + 1) >= 0 and(colonna + 1) <= 7:
				self.mosse_cavallo.append(indietro_sinistra)
				
			if (riga - 1) >= 0 and (riga - 1) <= 7 and (colonna + 2) >= 0 and (colonna + 2) <= 7:
				self.mosse_cavallo.append(destra_avanti)
			
			if (riga - 1) >= 0 and (riga - 1) <= 7 and (colonna - 2) >= 0 and (colonna - 2) <= 7:
				self.mosse_cavallo.append(destra_indietro)
			
			if (riga + 1) >= 0 and (riga + 1) <= 7 and (colonna + 2) >= 0 and (colonna + 2) <= 7:
				self.mosse_cavallo.append(sinistra_avanti)
			
			if (riga + 1) >= 0 and (riga + 1) <= 7 and (colonna - 2) >= 0 and (colonna - 2) <= 7:
				self.mosse_cavallo.append(sinistra_indietro)
			
		else:
			avanti_sinistra = ((riga - 2) * 8) + (colonna - 1)
			avanti_destra = ((riga - 2) * 8) + (colonna + 1)
			
			indietro_destra = ((riga + 2) * 8) + (colonna - 1)
			indietro_sinistra =	((riga + 2) * 8) + (colonna + 1)
			
			destra_avanti = ((riga - 1) * 8) + (colonna + 2)
			destra_indietro = ((riga - 1) * 8) + (colonna - 2)
			
			sinistra_avanti = ((riga + 1) * 8) + (colonna + 2)
			sinistra_indietro = ((riga + 1) * 8) + (colonna - 2)
			
			if (riga - 2) >= 0 and (riga - 2) <= 7 and (colonna - 1) >= 0 and (colonna - 1) <= 7:
				self.mosse_cavallo.append(avanti_sinistra)
			
			if (riga - 2) >= 0 and (riga - 2) <= 7 and (colonna + 1) >= 0 and (colonna + 1) <= 7:
				self.mosse_cavallo.append(avanti_destra)
			
			if (riga + 2) >= 0 and (riga + 2) <= 7 and (colonna - 1) >= 0 and (colonna - 1) <= 7:
				self.mosse_cavallo.append(indietro_destra)
			
			if (riga + 2) >= 0 and (riga + 2) <= 7 and (colonna + 1) >= 0 and(colonna + 1) <= 7:
				self.mosse_cavallo.append(indietro_sinistra)
				
			if (riga - 1) >= 0 and (riga - 1) <= 7 and (colonna + 2) >= 0 and (colonna + 2) <= 7:
				self.mosse_cavallo.append(destra_avanti)
			
			if (riga - 1) >= 0 and (riga - 1) <= 7 and (colonna - 2) >= 0 and (colonna - 2) <= 7:
				self.mosse_cavallo.append(destra_indietro)
			
			if (riga + 1) >= 0 and (riga + 1) <= 7 and (colonna + 2) >= 0 and (colonna + 2) <= 7:
				self.mosse_cavallo.append(sinistra_avanti)
			
			if (riga + 1) >= 0 and (riga + 1) <= 7 and (colonna - 2) >= 0 and (colonna - 2) <= 7:
				self.mosse_cavallo.append(sinistra_indietro)
	
	def check_play_bishop(self, clicked, riga, colonna):
		self.mosse_alfieri_ad = []
		self.mosse_alfieri_as = []
		self.mosse_alfieri_bd = []
		self.mosse_alfieri_bs = []
		
		for i in range(8):
			if (riga - i) >= 0 and (riga - i) <= 7 and (colonna + i) >= 0 and (colonna + i) <= 7:
				self.mosse_alfieri_ad.append( ((riga - i) * 8) + (colonna + i) )
		
		for i in range(8):
			if (riga - i) >= 0 and (riga - i) <= 7 and (colonna - i) >= 0 and (colonna - i) <= 7:
				self.mosse_alfieri_as.append( ((riga - i) * 8) + (colonna - i) )
		
		for i in range(8):
			if (riga + i) >= 0 and (riga + i) <= 7 and (colonna - i) >= 0 and (colonna - i) <= 7:
				self.mosse_alfieri_bd.append( ((riga + i) * 8) + (colonna - i) )
		
		for i in range(8):
			if (riga + i) >= 0 and (riga + i) <= 7 and (colonna + i) >= 0 and (colonna + i) <= 7:
				self.mosse_alfieri_bs.append( ((riga + i) * 8) + (colonna + i) )
	
	def check_play_queen(self, clicked, riga, colonna):
		self.mosse_queen_ra = []
		self.mosse_quuen_ri = []
		self.mosse_quuen_rd = []
		self.mosse_quuen_rs = []
		
		self.mosse_queen_dad = []
		self.mosse_queen_das = []
		self.mosse_queen_dbd = []
		self.mosse_queen_dbs = []
		
		#avanti
		for n in range(riga+1):
			self.mosse_queen_ra.append(((riga - n) * 8) + colonna)
		
		#destra
		for c in range(8-colonna):
			self.mosse_quuen_ri.append(((riga) * 8) + (colonna + c))
		
		#indietro
		for n in range(8-riga):
			self.mosse_quuen_rd.append(((riga + n) * 8) + colonna)
		
		#sinistra
		for c in range(colonna + 1):
			self.mosse_quuen_rs.append(((riga) * 8) + (c))
		
		#mosse diagonali
		for i in range(8):
			if (riga - i) >= 0 and (riga - i) <= 7 and (colonna + i) >= 0 and (colonna + i) <= 7:
				self.mosse_queen_dad.append( ((riga - i) * 8) + (colonna + i) )
		
		for i in range(8):
			if (riga - i) >= 0 and (riga - i) <= 7 and (colonna - i) >= 0 and (colonna - i) <= 7:
				self.mosse_queen_das.append( ((riga - i) * 8) + (colonna - i) )
		
		for i in range(8):
			if (riga + i) >= 0 and (riga + i) <= 7 and (colonna - i) >= 0 and (colonna - i) <= 7:
				self.mosse_queen_dbd.append( ((riga + i) * 8) + (colonna - i) )
		
		for i in range(8):
			if (riga + i) >= 0 and (riga + i) <= 7 and (colonna + i) >= 0 and (colonna + i) <= 7:
				self.mosse_queen_dbs.append( ((riga + i) * 8) + (colonna + i) )
		
			
	def check_if_pedon_can_eat(self, clicked, riga, colonna):
		if self.quadrati_campo[clicked]["fg"] == "white":
			
			for mp in self.mosse_pedoni:
				if self.quadrati_campo[mp]["fg"] == "black" or self.quadrati_campo[mp]["fg"] == "white":
					self.quadrati_campo[mp]["state"] = "disable"
					
			if colonna + 1 >= 0 and colonna + 1 <= 7:
				diagonale_amica_destra = ((riga - 1) * 8) + colonna + 1
				
				if self.quadrati_campo[diagonale_amica_destra]["fg"] == "black":
					self.quadrati_campo[diagonale_amica_destra]["state"] = "normal"
			
			if colonna - 1 >= 0 and colonna - 1 <= 7:
				diagonale_amica_sinistra = ((riga - 1) * 8) + colonna - 1
				
				if self.quadrati_campo[diagonale_amica_sinistra]["fg"] == "black":
				 	self.quadrati_campo[diagonale_amica_sinistra]["state"] = "normal"
				
		else:
			for mp in self.mosse_pedoni:
				if self.quadrati_campo[mp]["fg"] == "black" or self.quadrati_campo[mp]["fg"] == "white":
					self.quadrati_campo[mp]["state"] = "disable"
			
			if colonna + 1 >= 0 and colonna + 1 <= 7:
				diagonale_nemica_destra = ((riga + 1) * 8) + colonna + 1
				
				if self.quadrati_campo[diagonale_nemica_destra]["fg"] == "white":
					self.quadrati_campo[diagonale_nemica_destra]["state"] = "normal"
			
			if colonna - 1 >= 0 and colonna - 1 <= 7:
				diagonale_nemica_sinistra = ((riga + 1) * 8) + colonna - 1
			
				if self.quadrati_campo[diagonale_nemica_sinistra]["fg"] == "white":
				 	self.quadrati_campo[diagonale_nemica_sinistra]["state"] = "normal"
	
	def check_if_king_can_eat(self, se_stesso):
		if self.quadrati_campo[se_stesso]["fg"] == "white":
		
			for play_k in self.mosse_re:
				if self.quadrati_campo[play_k]["fg"] == "white" and self.quadrati_campo[play_k] != self.quadrati_campo[se_stesso]:
					self.quadrati_campo[play_k]["state"] = "disable"
					
				if self.quadrati_campo[play_k]["fg"] == "black":
					self.quadrati_campo[play_k]["state"] = "normal"
		else:
		
			for play_k in self.mosse_re:
				if self.quadrati_campo[play_k]["fg"] == "black" and self.quadrati_campo[play_k] != self.quadrati_campo[se_stesso]:
					self.quadrati_campo[play_k]["state"] = "disable"
					
				if self.quadrati_campo[play_k]["fg"] == "white":
					self.quadrati_campo[play_k]["state"] = "normal"
	
	def check_if_tower_can_eat(self, se_stesso):
		flag_amico = False
		flag_nemico = False
		do_not_touch = False
		mosse_t = [self.mosse_torri_a, self.mosse_torri_i, self.mosse_torri_d, self.mosse_torri_s]
		self.mosse_torri_s = self.mosse_torri_s.reverse() if len(self.mosse_torri_s) > 1 else self.mosse_torri_s
		
		if self.quadrati_campo[se_stesso]["fg"] == "white":
			amico = "white"
			nemico = "black"
		else:
			amico = "black"
			nemico = "white"
			
		for i in range(4):
			flag_amico = False
			flag_nemico = False
			
			for x in mosse_t[i]:
				do_not_touch = False
				if self.quadrati_campo[x]["fg"] == amico and self.quadrati_campo[x]["bg"] == "gray":
					self.quadrati_campo[x]["state"] = "disable"
					flag_amico = True
					
				if flag_amico == True:
					self.quadrati_campo[x]["state"] = "disable"
				
				if self.quadrati_campo[x]["fg"] == nemico and self.quadrati_campo[x]["bg"] == "gray" and flag_amico != True:
					if flag_nemico != True:
						self.quadrati_campo[x]["state"] = "normal"
						do_not_touch = True
					flag_nemico = True
						
				if flag_nemico == True and do_not_touch != True:
					self.quadrati_campo[x]["state"] = "disable"
	
	def check_if_horse_can_eat(self, se_stesso):
		
		if self.quadrati_campo[se_stesso]["fg"] == "white":
			amico = "white"
			nemico = "black"
		else:
			amico = "black"
			nemico = "white"
		
		for x in self.mosse_cavallo:
			if self.quadrati_campo[x]["bg"] == "gray" and self.quadrati_campo[x]["fg"] == amico:
				self.quadrati_campo[x]["state"] = "disable"
			
			if self.quadrati_campo[x]["bg"] == "gray" and self.quadrati_campo[x]["fg"] == nemico:
				self.quadrati_campo[x]["state"] = "normal"
	
	def check_if_bishop_can_eat(self, se_stesso):
		flag_amico = False
		flag_nemico = False
		do_not_touch = False
		mosse_a = [self.mosse_alfieri_ad, self.mosse_alfieri_as, self.mosse_alfieri_bd, self.mosse_alfieri_bs]
		
		if self.quadrati_campo[se_stesso]["fg"] == "white":
			amico = "white"
			nemico = "black"
		else:
			amico = "black"
			nemico = "white"
			
		for i in range(4):
			flag_amico = False
			flag_nemico = False
			
			for x in mosse_a[i]:
				do_not_touch = False
				if self.quadrati_campo[x]["fg"] == amico and self.quadrati_campo[x]["bg"] == "gray":
					self.quadrati_campo[x]["state"] = "disable"
					flag_amico = True
					
				if flag_amico == True:
					self.quadrati_campo[x]["state"] = "disable"
				
				if self.quadrati_campo[x]["fg"] == nemico and self.quadrati_campo[x]["bg"] == "gray" and flag_amico != True:
					if flag_nemico != True:
						self.quadrati_campo[x]["state"] = "normal"
						do_not_touch = True
					flag_nemico = True
						
				if flag_nemico == True and do_not_touch != True:
					self.quadrati_campo[x]["state"] = "disable"
					
	def check_if_queen_can_eat(self, se_stesso):
		flag_amico = False
		flag_nemico = False
		do_not_touch = False
		
		mosse_o = [self.mosse_queen_ra, self.mosse_quuen_ri, self.mosse_quuen_rd, self.mosse_quuen_rs]
		self.mosse_quuen_rs = self.mosse_quuen_rs.reverse() if len(self.mosse_quuen_rs) > 1 else self.mosse_quuen_rs
		
		if self.quadrati_campo[se_stesso]["fg"] == "white":
			amico = "white"
			nemico = "black"
		else:
			amico = "black"
			nemico = "white"
			
		for i in range(4):
			flag_amico = False
			flag_nemico = False
			
			for x in mosse_o[i]:
				do_not_touch = False
				if self.quadrati_campo[x]["fg"] == amico and self.quadrati_campo[x]["bg"] == "gray":
					self.quadrati_campo[x]["state"] = "disable"
					flag_amico = True
					
				if flag_amico == True:
					self.quadrati_campo[x]["state"] = "disable"
				
				if self.quadrati_campo[x]["fg"] == nemico and self.quadrati_campo[x]["bg"] == "gray" and flag_amico != True:
					if flag_nemico != True:
						self.quadrati_campo[x]["state"] = "normal"
						do_not_touch = True
					flag_nemico = True
						
				if flag_nemico == True and do_not_touch != True:
					self.quadrati_campo[x]["state"] = "disable"
		
		#controllo  obliquo
		flag_amico = False
		flag_nemico = False
		do_not_touch = False
		mosse_d = [self.mosse_queen_dad,  self.mosse_queen_das, self.mosse_queen_dbd, self.mosse_queen_dbs]
		
		if self.quadrati_campo[se_stesso]["fg"] == "white":
			amico = "white"
			nemico = "black"
		else:
			amico = "black"
			nemico = "white"
			
		for i in range(4):
			flag_amico = False
			flag_nemico = False
			
			for x in mosse_d[i]:
				do_not_touch = False
				if self.quadrati_campo[x]["fg"] == amico and self.quadrati_campo[x]["bg"] == "gray":
					self.quadrati_campo[x]["state"] = "disable"
					flag_amico = True
					
				if flag_amico == True:
					self.quadrati_campo[x]["state"] = "disable"
				
				if self.quadrati_campo[x]["fg"] == nemico and self.quadrati_campo[x]["bg"] == "gray" and flag_amico != True:
					if flag_nemico != True:
						self.quadrati_campo[x]["state"] = "normal"
						do_not_touch = True
					flag_nemico = True
						
				if flag_nemico == True and do_not_touch != True:
					self.quadrati_campo[x]["state"] = "disable"
		
def main():
	sc = campo_scacchi()
	sc.mainloop()

main()
