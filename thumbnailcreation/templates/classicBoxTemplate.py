from typing import Dict
from .templateInterface import Template
from .helpers import image_resize_helper, default_maximums_helper
from PIL import Image, ImageDraw, ImageFont

class classicBoxTemplate(Template):
	def __init__(self):
		self.config["order"] = ["section_1", "section_2", "image_1", "image_2"]
		## SECTION_1
		self.config["section_1"]["boxcolor"] = "#FFFFFF"
		self.config["section_1"]["boxside"] = "left"
		self.config["section_1"]["line1_color"]= "#000000"
		self.config["section_1"]["line1_font"]= "calibrib"
		self.config["section_1"]["line2_color"]= "#000000"
		self.config["section_1"]["line2_font"]= "calibri"
		self.config["section_1"]["line3_color"]= "#000000"
		self.config["section_1"]["line3_font"]= "calibrib"
		#Spaces outside the box
		self.config["section_1"]["topspace"] = 20
		self.config["section_1"]["middlespace"] = 20
		self.config["section_1"]["borderspace"] = 20
		#margin inside the box
		self.config["section_1"]["topmargin"] = 13
		self.config["section_1"]["sidemargin"] = 20
		self.config["section_1"]["bottommargin"] = 13
		# minimum width and height
		self.config["section_1"]["default_content_height"] = 94  # Default Content height without margin
		self.config["section_1"]["default_box_width"] = 500
		self.config["section_1"]["logospace"] = 0
		## LOGO
		self.config["logo"]["minimum_height"] = 94
		self.config["logo"]["maximum_height"] = 150
		## SECTION 2
		self.config["section_2"]["boxcolor"] = "#FFFFFF"
		self.config["section_2"]["boxside"] = "right"
		self.config["section_2"]["line1_color"]= "#000000"
		self.config["section_2"]["line1_font"]= "calibri"
		self.config["section_2"]["line2_color"]= "#000000"
		self.config["section_2"]["line2_font"]= "calibrib"
		self.config["section_2"]["line3_color"]= "#000000"
		self.config["section_2"]["line3_font"]= "calibrib"
		#Spaces outside the box
		self.config["section_2"]["topspace"] = 20
		self.config["section_2"]["middlespace"] = 20
		self.config["section_2"]["borderspace"] = 20
		self.config["section_2"]["bottomspace"] = 75
		#margin inside the box
		self.config["section_2"]["topmargin"] = 15
		self.config["section_2"]["sidemargin"] = 17
		self.config["section_2"]["bottommargin"] = 20
		# minimum width and height
		self.config["section_2"]["default_content_height"] = 166  # Default Content height without margin
		self.config["section_2"]["default_box_width"] = 640
		## IMAGE_1
		self.config["image_1"]["side"] = "right"
		self.config["image_1"]["maximum_height"] = 250
		self.config["image_1"]["topmargin"] = 20
		self.config["image_1"]["sidemargin"] = 20
		## IMAGE_2
		self.config["image_2"]["side"] = "left"
		self.config["image_2"]["maximum_height"] = 250
		self.config["image_2"]["topmargin"] = 20
		self.config["image_2"]["sidemargin"] = 80
		self.config["image_2"]["bottommargin"] = 95
		
	def create_thumbnail(self, img: Image, data: Dict) -> Image:
		self.config = default_maximums_helper(img, self.config)
		if data["image_1"]["activate"]:
			img = self.add_picture_1(img, data["image_1"])

		if data["image_2"]["activate"]:
			img = self.add_picture_2(img, data["image_2"])

		if data["section_1"]["activate"]:
			img = self.upper_box(img, data["section_1"], data["logo"])

		if data["section_2"]["activate"]:
			img = self.down_box(img, data["section_2"])
		return img

	def upper_box(self, img: Image, data: Dict, logodata: Dict) -> Image:
		""" Draw upper Box with choosen data"""

		line1_font = ImageFont.truetype(data["line1_font"], 28)
		line1_size = line1_font.getsize(data["line1_text"])
		line2_font = ImageFont.truetype(data["line2_font"], 28)
		line2_size = line2_font.getsize(data["line2_text"])
		line3_font = ImageFont.truetype(data["line3_font"], 28)
		line3_size = line3_font.getsize(data["line3_text"])
		max_linelen = max([line1_size[0], line2_size[0], line3_size[0]])

		# LogoWork
		if logodata["activate"]:
			logo = Image.open(logodata["logopath"])
			logo = image_resize_helper(logodata, logo)
			data["logospace"] = logo.width + 13
			if logo.height > data["default_content_height"]:
				data["default_content_height"] = logo.height
		else: 
			logo = None


		rectwidth = max_linelen + data["topspace"] + data["middlespace"] + data["logospace"]
		if rectwidth < data["default_box_width"]:
			rectwidth = data["default_box_width"]
		rectheight = data["default_content_height"] + data["topmargin"] + data["bottommargin"]

		# Boxposition on left
		if data["boxside"] == "left":
			x1 = 0-data["borderspace"]
			y1 = data["topspace"]
			x2 = rectwidth
			y2 = data["topspace"] + rectheight
			box_border_on_image = x1 + data["borderspace"]

		# Boxposition on right
		else:
			x1 = img.width-rectwidth
			y1 = data["topspace"]
			x2 = img.width + data["borderspace"]
			y2 = data["topspace"] + rectheight
			box_border_on_image = x1
			
		#Rectangle
		drawing = ImageDraw.Draw(img)
		drawing.rounded_rectangle([(x1, y1), (x2, y2)], radius=15, fill=data["boxcolor"], outline=None, width=1)
		#Draw Logo
		if logo:
			logo_x = box_border_on_image + data["sidemargin"]
			if logo.height < data["default_content_height"]:
				logo_y = round(data["topspace"] + data["topmargin"] + (data["default_content_height"] - logo.height) / 2)
			else: logo_y = data["topspace"] + data["topmargin"]
			img.paste(logo, (logo_x, logo_y))
		
		# Line1
		line_x = box_border_on_image + data["sidemargin"] + data["logospace"]
		line1_y = y1 + data["topmargin"]
		drawing.text((line_x, line1_y), data["line1_text"], font=line1_font, fill=data["line1_color"])

		# Line 3
		line3_y = y2 - data["bottommargin"]
		drawing.text((line_x, line3_y), data["line3_text"], anchor="ls", font=line3_font, fill=data["line3_color"])

		# Line2
		drawing.text((line_x, y2-data["bottommargin"] - line1_font.getsize("o")[1]), data["line2_text"], anchor="lb", font=line2_font, fill=data["line2_color"])
		
		logo.close()
		return img

	def down_box(self, img: Image, data: Dict) -> Image:
		""" Draw downer Box with choosen data"""
		line1_font = ImageFont.truetype(data["line1_font"], 45)
		line1_size = line1_font.getsize(data["line1_text"])
		line2_font = ImageFont.truetype(data["line2_font"], 55)
		line2_size = line2_font.getsize(data["line2_text"])
		line3_font = ImageFont.truetype(data["line3_font"], 55)
		line3_size = line3_font.getsize(data["line3_text"])
		max_linelen = max([line1_size[0], line2_size[0], line3_size[0]])

		rectwidth = max_linelen + data["topspace"] + data["middlespace"]
		if rectwidth < data["default_box_width"]:
			rectwidth = data["default_box_width"]
		rectheight = data["default_content_height"] + data["topmargin"] + data["bottommargin"]

		# Boxposition on left
		if data["boxside"] == "left":
			x1 = 0-data["borderspace"]
			y1 = img.height - data["bottomspace"] - rectheight - data["topspace"]
			x2 = rectwidth
			y2 = y1 + rectheight
			box_border_on_image = x1 + data["borderspace"]

		# Boxposition on right
		else:
			x1 = img.width-rectwidth
			y1 = img.height - data["bottomspace"] - rectheight - data["topspace"]
			x2 = img.width + data["borderspace"]
			y2 = y1 + rectheight
			box_border_on_image = x1
			
		#Rectangle
		drawing = ImageDraw.Draw(img)
		drawing.rounded_rectangle([(x1, y1), (x2, y2)], radius=15, fill=data["boxcolor"], outline=None, width=1)
		
		# Line1
		line_x = box_border_on_image + data["sidemargin"]
		line1_y = y1 + data["topmargin"]
		drawing.text((line_x, line1_y), data["line1_text"], font=line1_font, fill=data["line1_color"])

		# Line 3
		line3_y = y2 - data["bottommargin"]
		drawing.text((line_x, line3_y), data["line3_text"], anchor="ls", font=line3_font, fill=data["line3_color"])

		# Line2
		drawing.text((line_x, y2-data["bottommargin"] - line1_font.getsize("y2")[1]-14), data["line2_text"], anchor="lb", font=line2_font, fill=data["line2_color"])
		
		return img

	def add_picture_1(self, img: Image, data: Dict) -> Image:
		pic = Image.open(data["imagepath"])
		pic = image_resize_helper(data, pic)

		if data["side"] == "left":
			x = data["sidemargin"]
			y = data["topmargin"]
		else:
			x = img.width - pic.width - data["sidemargin"]
			y = data["topmargin"]
		img.paste(pic, (x, y))

		pic.close()
		return img

	def add_picture_2(self, img: Image, data: Dict) -> Image:
		pic = Image.open(data["imagepath"])
		pic = image_resize_helper(data, pic)

		if data["side"] == "left":
			x = data["sidemargin"]
			y = img.height - pic.height - data["bottommargin"]
		else:
			x = img.width - pic.width - data["sidemargin"]
			y = img.height - pic.height - data["bottommargin"]
		img.paste(pic, (x, y))

		pic.close()
		return img