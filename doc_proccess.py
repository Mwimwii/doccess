import os, sys
from PIL import Image 
import pytesseract as pyt
from time import sleep
# from .lib/scan import scan
BASE_DIR = os.getcwd()
	
# pyt.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'



def parseString(curr_str):
	text = curr_str.split('\n')
	# for

def scanImage(curr_img, box_areas):
	results = {}

	for cl_index in range(len(box_areas)):
		# print('SCANNING upper:{}'.format(cl_index))
		#crop the image
		img_selection = curr_img.crop(box_areas[cl_index])
		#save as temp
		dithered = img_selection.convert('1', dither=Image.NONE)
		dithered.save('amp{}.jpg'.format(cl_index))
		load_selection = Image.open('amp{}.jpg'.format(cl_index))
		scanned_string = pyt.image_to_string(load_selection)

		coord = ".".join([str(i) for i in box_areas[cl_index]])
		try:
		  find_digit =  ([i for i in scanned_string.split('\n') if i.isdigit()])[0]
		  scan_to_int = int(find_digit)
		  # scan_to_int = int(scanned_string)
		  results[coord] = dict(page_number = find_digit, string_used = scanned_string)
		  # results[cl_index] = dict(page_number = find_digit, string_used = scanned_string.replace('\n',' '))
		except (ValueError, IndexError):
			pass
			# results[coord] = dict(string_used = scanned_string)
			# results[cl_index] = dict(string_used = scanned_string.replace('\n',' '))
			# print(box_areas[cl_index])
	# print (results)
	return results

def find_resolution(curr_img_path):
	curr_img = Image.open(curr_img_path)
	return curr_img.size

def get_partitions(size_total, partitions, top, bot, bias=100):
	"""
		A list of lists of scan areas for the entire thing this is 
		by getting the resolution of the image provided and finding the 
		apporpriate sections that it can be divided into thus 
		appending the crop list.
	"""
	temp_list = []
	origin_crop = 0,size_total
	partsize = int(origin_crop[1]/partitions) + bias
	rstart = list(range(0,int(origin_crop[1]),partsize))
	remainder = (int(origin_crop[1]%partitions))

	for partition in range(0, partitions):
		temp_list.append([rstart[partition], top, rstart[partition]+ partsize, bot])
	if (remainder):
		temp_list.append([origin_crop[1]-remainder, top, origin_crop[1] , bot])
	return(temp_list)

#set file paths
filepath = os.path.join(BASE_DIR, 'files')
files    = os.listdir(filepath)

#declarations
if (len(files)>0):
	w, h  = find_resolution(os.path.join(filepath, files[0]))
upper, lower = 0, h/6
no_part = 1
crop_list = get_partitions(w, no_part, upper, lower)
img_read =[]
in_range = 50
#create folder called render 
output_path = os.path.join(BASE_DIR, 'output3')
try:
	os.mkdir(output_path)
except:
	pass
#place all the 

print ('BLOCK SIZE: {}px\nHEIGHT: {}px'.format(w/no_part, lower))

file_length = len(files)
for images_cont in range(0,in_range):
# for images_cont in range(file_length):
	print('PAGE{} : {}'.format(images_cont, files[images_cont]))
	curr_scan_image = Image.open(os.path.join(filepath, files[images_cont]))
	# \/\/\/\/\/\/\/ DONTREMOVE \/\/\/\/\/\/\/
	img_read.append(scanImage(curr_scan_image, crop_list))

	try:
		page_title =(list(img_read[images_cont].values())[0]['page_number'])
		if (int(page_title)>40):
			curr_scan_image.save(output_path+'/'+page_title+'.jpg') 
		else:
			page_title = 'failed_{}'.format(images_cont)	
			curr_scan_image.save(output_path+'/'+page_title+'.jpg')
	except:
		page_title = 'failed_{}'.format(images_cont)
		curr_scan_image.save(output_path+'/'+page_title+'.jpg')
	# sys.stdout.write('\r')
	# sys.stdout.write('SCANNING : %d/%d' %(images_cont, len(files)))
	# sys.stdout.flush
print (img_read)
valid_pages = [i for i in img_read if i != {}]
accuracy = (float(len(valid_pages))/float(in_range))*100
print('\n{} out of {} non-empty scans\nACCURACY: {:0.2f}%'.format(len(valid_pages), in_range, accuracy))


