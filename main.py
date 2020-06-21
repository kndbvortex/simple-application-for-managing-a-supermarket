from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QDialog, QMessageBox, QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QPixmap, QStandardItemModel
from PyQt5 import QtCore
import sys
from pickle import Pickler, Unpickler
from marche import *


class Marche(QMainWindow):
	"""Classe qui gère le super marche"""
	def __init__(self):
		super().__init__()
		self.nom_fichier = "article_magasin"
		self.mot_de_passe = {"kndb":"vortex","":""}
		self.ui = Ui_SuperMarche()
		self.ui.setupUi(self)
		self.set_actions()


	def set_actions(self):
		self.ui.label_visibilite_pass.mousePressEvent = self.visibilite_mot_passe
		self.ui.bouton_connexion.clicked.connect(self.connexion)
		self.ui.bouton_liste_article.clicked.connect(lambda : self.afficher_liste_produit())
		self.ui.bouton_ajouter_article.clicked.connect(lambda : self.ui.stackedWidget_2.setCurrentIndex(2))
		self.ui.bouton_modifier_article.clicked.connect(lambda : self.ui.stackedWidget_2.setCurrentIndex(3))
		self.ui.bouton_supprimer_article.clicked.connect(lambda : self.ui.stackedWidget_2.setCurrentIndex(4))
		self.ui.bouton_valider_ajouter_article.clicked.connect(lambda : self.ajouter())


	def visibilite_mot_passe(self, event):
		if self.ui.lineEdit_mot_de_passe.echoMode() == QLineEdit.Normal :
			self.ui.lineEdit_mot_de_passe.setEchoMode(QLineEdit.Password)
			self.ui.label_visibilite_pass.setToolTip("Afficher le mot de passe")
			self.ui.label_visibilite_pass.setPixmap(QPixmap("images/interface.png"))
		else :
			self.ui.lineEdit_mot_de_passe.setEchoMode(QLineEdit.Normal)
			self.ui.label_visibilite_pass.setToolTip("Cacher le mot de passe")
			self.ui.label_visibilite_pass.setPixmap(QPixmap("images/diagonal.png"))

	def connexion(self):
		nom_utilisateur = self.ui.lineEdit_nom_utilisateur.text()
		mot_de_passe = self.ui.lineEdit_mot_de_passe.text()
		if nom_utilisateur in self.mot_de_passe:
			if self.mot_de_passe[nom_utilisateur] == mot_de_passe:
				self.ui.stackedWidget.setCurrentIndex(1)
			else : 
				self.ui.label_information_connexion.setText("Le nom et le Mot de passe ne correspondent pas")
				self.ui.label_information_connexion.setStyleSheet("background-color : #c0392b;color : white;\
					font: 14pt 'Ubuntu Condensed';")
		else : 
			self.ui.label_information_connexion.setText("Le nom et le Mot de passe ne correspondent pas")
			self.ui.label_information_connexion.setStyleSheet("background-color : #c0392b;color : white;\
				font: 14pt 'Ubuntu Condensed';")


	def afficher_liste_produit(self):
		self.ui.stackedWidget_2.setCurrentIndex(1)
		liste_article = dict()
		ok = False

		while ok == False:
			try:
				liste_article = self.dictionnaire_articles_magasin()
				ok = True
			except FileNotFoundError :
				with open(self.nom_fichier, "wb"):
					pass
		if liste_article == {} :
			QMessageBox.information(self, "Liste des article", "Aucun article dans le magasin veuillez\
									en ajouter au préalable")
		else:
			self.ui.tableWidget.setRowCount(len(liste_article))
			self.ui.tableWidget.setColumnCount(2)
			self.ui.tableWidget.setHorizontalHeaderLabels(["Nom", "Quantite"])
			self.ui.tableWidget.verticalHeader().hide()
			i = 0
			for nom,quantite in liste_article.items() : 
				self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(nom))
				self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(quantite)))
				i += 1
			for i in range(self.ui.tableWidget.rowCount()):
				for j in range (self.ui.tableWidget.columnCount()):
					self.ui.tableWidget.item(i,j).setTextAlignment(QtCore.Qt.AlignHCenter)

			for i in range(self.ui.tableWidget.columnCount()):
				self.ui.tableWidget.setColumnWidth(i,self.ui.tableWidget.width()/2)

			self.ui.tableWidget.setShowGrid(False)


	def dictionnaire_articles_magasin(self):
		liste_article = dict()
		with open(self.nom_fichier, "rb") as fichier:
			u = Unpickler(fichier)
			liste_article = u.load()
		return liste_article


	def ajouter_article(self, nom, quantite):
		ok = False
		while not ok:
			try :
				liste_article = self.dictionnaire_articles_magasin()	

				if  nom in liste_article and liste_article != {}:
					QMessageBox.information(self, 'Ajout',\
					 "Ce produit existe déjà dans le magasin pensez plutot à le modifier....")
				else:
					liste_article = dict(**liste_article, **{nom:quantite})
					
					with open (self.nom_fichier, "wb") as fichier :
						p = Pickler(fichier)
						p.dump(liste_article)
					QMessageBox.information(self, 'Ajout',"Ce produit a été ajouté avec succès....")
				ok = True
			
			except FileNotFoundError :
				with open(self.nom_fichier, "wb"):
					pass


	def ajouter(self):
		nom = self.ui.lineEdit_nom_article_ajouter.text()
		quantite = self.ui.spinBox_quantite_article_ajouter.value()
		if nom == "":
			QMessageBox.critical(self, 'Ajout',"Nom de produit invalide")
		elif quantite == 0:
			QMessageBox.critical(self, 'Ajout',"La quantité d'un nouveau produit de saurait être nulle")
		else:
			self.ajouter_article(nom,quantite)
			self.ui.lineEdit_nom_article_ajouter.setText("")
			self.ui.spinBox_quantite_article_ajouter.setValue(0)


def main():
	appli = QApplication(sys.argv)
	window = Marche()
	window.show()
	sys.exit(appli.exec_())


if __name__ == '__main__':
	main()
