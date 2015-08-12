__version__ = '1.0'

from kivy.app import App
from kivy.config import Config
Config.set('graphics','width','450')
Config.set('graphics','height','800')
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.label import Label
import time
from genSeq import *


class ExitButton(Button):
	def __init__(self,**kwargs):
		super(ExitButton,self).__init__(**kwargs);
		self.size=(70,50);
		self.text=("Exit");
	def on_release(self):
		exit();
	
class ResetButton(Button):
	def __init__(self,**kwargs):
		super(ResetButton,self).__init__(**kwargs);
		self.size=(100,50)
		self.text=("Reset Game");
	def on_release(self):
		for square in self.parent.controller.arrSeqSquares:
			self.parent.remove_widget(square);	
		self.parent.draw();
		self.parent.controller.state='endGame';
		self.parent.controller.ResetSeq();
		
class StartButton(Button):
	def __init__(self, **kwargs):
		super(StartButton,self).__init__(**kwargs);
		self.size=(100,50);
		self.text=("Start Game");
	def on_release(self):
		self.parent.controller.state='initAnimation';
		if self.parent.level>7:
			self.parent.controller.arrSeq=genSeq1(self.parent.n);
		else:
			self.parent.controller.arrSeq=genSeq2(self.parent.n);
		self.parent.controller.ResetSeq();
		self.parent.controller.tries=0;
		Clock.schedule_interval(self.parent.controller.action, 1.0);
		
class PopupMessage(Popup):
	def __init__(self,**kwargs):
		super(PopupMessage,self).__init__(**kwargs);
		self.title_size=30;
		self.size_hint=(0.6,0.4);
	def win(self):
		self.title='You Won!';
		label='Congratulations! You successfully completed the level.'+'\n'+'\n'+'Press "Start Game" to play again.'
		content=Label(text=label,text_size=(170,None));
		self.content=content;
	def lose(self):
		self.title='You Lost!';
		label='You failed the level!'+'\n'+'\n'+'Press "Start Game" to play again.'
		content=Label(text=label,text_size=(170,None));
		self.content=content;
	def retry(self):
		self.title='WRONG!';
		label='You clicked the wrong square!'+'\n'+'\n'+'You will have one more try.'
		content=Label(text=label,text_size=(170,None));
		self.content=content;

class Square(Widget):
	def __init__(self, **kwargs):
		super(Square,self).__init__(**kwargs);
		self.color=kwargs['color'];
		self.bind(pos=self.draw);
		self.bind(size=self.draw);
	def draw(self, *args):
		with self.canvas:
			Color(*self.color);
			Rectangle(pos=self.pos, size=self.size);
	def on_touch_down(self, touch):
		if touch.x<self.pos[0] + self.width and touch.x>self.pos[0]:
			if touch.y<self.pos[1] + self.height and touch.y>self.pos[1]:
				if self.parent.controller.canClick:
					if self.parent.controller.checkClick(self.pos):
						with self.canvas:
							Color(0,.7,0);
							Rectangle(pos=self.pos,size=self.size);

class Grid(Widget):
	def __init__(self, **kwargs):
		super(Grid,self).__init__(**kwargs);
		self.controller=kwargs['controller'];
		self.n=kwargs['n'];
		self.squareSize=kwargs['sqsize'];
		self.level=1;
		self.arrSquares=[];
		self.pos_x=0;	self.pos_y=0;
		self.boardDrawn=False;
		self.resetbutton=ResetButton();
		self.startbutton=StartButton();
		self.add_widget(self.resetbutton);
		self.add_widget(self.startbutton);
		self.add_widget(ExitButton());
		self.label_level=Label(text='Level '+str(self.level),font_size='50sp');
		self.add_widget(self.label_level);
		self.bind(pos=self.setPos);
		self.bind(size=self.setPos);				
	def setPos(self,*args):
		level = self.level;
		if 2<level<6:
			self.n=4;
		elif level>=6:
			self.n=5;
		if self.boardDrawn==False:
			boardsize=(self.squareSize+5)*self.n-5;
			self.pos_x=(self.right-boardsize)/2;
			self.pos_y=(self.top-boardsize)/2;
			self.drawBoard();
		offset=self.resetbutton.width;
		self.resetbutton.pos=(self.center_x-offset-70 , self.y+150);
		self.resetbutton.size=(self.width*0.25,75);
		self.startbutton.pos=(self.center_x+70, self.y+150);
		self.startbutton.size=(self.width*0.25,75);
		self.label_level.pos=(self.center_x-50,self.top-150);		
	def drawBoard(self):
		for x in range(0, self.n):
			for y in range(0, self.n):
				sq = Square(pos=(x*(self.squareSize+5)+self.pos_x,y*(self.squareSize+5)+self.pos_y),color=(1,1,1),size=(self.squareSize,self.squareSize));
				self.arrSquares.append(sq);
				self.add_widget(sq);
		self.label_start=Label(text='Start',font_size='18sp',pos=(self.pos_x,self.pos_y-40),size=(50,25),color=(1,1,1));
		self.label_finish=Label(text='Finish',font_size='18sp',pos=(self.right-self.pos_x-60,self.pos_y+((self.squareSize+5)*self.n-5)+15),size=(50,25),color=(1,1,1));
		self.add_widget(self.label_start);
		self.add_widget(self.label_finish);
		self.draw(); self.boardDrawn=True;		
	def nextLevel(self):
		for sq in self.arrSquares:
			self.remove_widget(sq);
		self.boardDrawn=False;
		self.remove_widget(self.label_start);
		self.remove_widget(self.label_finish);
		self.arrSquares=[]; self.level+=1;
		self.label_level.text='Level '+str(self.level);
		self.setPos();		
	def draw(self, *args):
		with self.canvas:
			for square in self.arrSquares:
				square.draw();

class Controller:
	def __init__(self):
		self.state=None;
		self.tries=0;
		self.setLevel=True;
		self.canClick=False;
		self.arrSeq=[];
		self.arrSeqSquares=[];
		self.arrSeqPositions=[];
		self.popupmessage=PopupMessage();
	def setGrid(self, Grid):
		self.grid = Grid;
	def action(self,dt):
		if self.state=="initAnimation":
			self.canClick=False;
			self.actionInitAnimation();
		elif self.state=="pauseAnimation":
			time.sleep(1.0);
			self.state='redrawAnimation';
		elif self.state=="redrawAnimation":
			if self.idx==0:
				for sq in self.arrSeqSquares:
					self.grid.remove_widget(sq);
			self.actionReDrawAnimation();
		elif self.state=="endAnimation":
			time.sleep(1.0);
			for sq in self.arrSeqSquares:
					self.grid.remove_widget(sq);
			self.canClick=True;
			self.state='waitForTouch';
		elif self.state=="failureAnimation":
			self.canClick=False;
			self.actionFailureAnimation();
		elif self.state=="successAnimation":
			self.actionSuccessAnimation();
		elif self.state=='waitForTouch': pass;
		elif self.state=='pauseGame': pass;
		elif self.state=='endGame':
			self.idx=0;	self.canClick=False;
			return False;
			
	def actionInitAnimation(self):
		pos=self.arrSeq[self.idx]; self.idx+=1;
		x=pos[0]; y=pos[1];
		sq = Square(pos=(x*(self.grid.squareSize+5)+self.grid.pos_x,y*(self.grid.squareSize+5)+self.grid.pos_y),color=(1,0,0),size=(self.grid.squareSize,self.grid.squareSize));
		self.arrSeqPositions.append(sq.pos);		
		self.arrSeqSquares.append(sq);
		self.grid.add_widget(sq); sq.draw();
		if self.idx==len(self.arrSeq): 
			self.idx=0;
			self.state='pauseAnimation';
	def actionReDrawAnimation(self):
		sq=self.arrSeqSquares[self.idx];
		self.grid.add_widget(sq); sq.draw();
		self.idx+=1;
		if self.idx==len(self.arrSeqSquares):
			self.idx=0;
			self.state='endAnimation';
	def checkClick(self, position):
		if len(self.arrSeqPositions)!=0:
			if position==self.arrSeqPositions[self.idx]:
				self.idx+=1;
				if self.idx==len(self.arrSeqPositions):
					self.state='successAnimation';
				return True;
			else:
				self.grid.draw(); self.idx=0;	self.tries+=1;
				self.state='pauseGame'; time.sleep(1.0);
				if self.tries<=1:
					self.popupmessage.retry();	self.popupmessage.open();
					self.popupmessage.bind(on_dismiss=self.resumeGame);
				else:
					self.state='endGame';
					self.popupmessage.lose();	self.popupmessage.open();
					self.popupmessage.bind(on_dismiss=self.ResetGame);
	def resumeGame(self,*args):
		self.state='failureAnimation';
	def actionFailureAnimation(self):
		sq=self.arrSeqSquares[self.idx];
		self.grid.add_widget(sq); sq.draw();
		self.idx+=1;
		if self.idx==len(self.arrSeqSquares):
			self.idx=0;
			self.state='endAnimation';
	def actionSuccessAnimation(self):
		self.state='endGame';
		self.setLevel=False;
		self.popupmessage.win();
		self.popupmessage.open();
		self.popupmessage.bind(on_dismiss=self.nextLevel);
	def nextLevel(self,*args):
		if self.setLevel==False:
			self.idx=0;	self.arrSeq=[];
			self.arrSeqSquares=[]; self.arrSeqPositions=[];
			self.grid.nextLevel();
			self.setLevel=True;
	def ResetSeq(self):
		self.idx=0;	self.canClick=False;
		self.arrSeqSquares=[]; self.arrSeqPositions=[];
	def ResetGame(self,*args):
		if self.setLevel==False:
			self.idx=0;
			self.arrSeqSquares=[]; self.arrSeqPositions=[];
			self.grid.draw();
	
		
class SequencingGameApp(App):
	def build(self):
		controller =  Controller();
		grid = Grid(n=3,sqsize=90,controller=controller);
		controller.setGrid(grid);
		return grid;


if __name__ == '__main__':
	SequencingGameApp().run()
