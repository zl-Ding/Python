from gradio_client import Client

json = "Chatbot.json"
path = "E://AllFile/Verysync/Data/KITTI/data_object_image_2/training/image_2/"
client = Client("https://efcfde3958b7f48dc9.gradio.live/")
result = client.predict(
				"Howdy!",	# str in 'Text' Textbox component
				# path+"000000.png",	# str (filepath or URL to image)
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",
								#in 'Image' Image component
				"https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav",	# str (filepath or URL to file)
							#	in 'parameter_14' Audio component
				"https://github.com/gradio-app/gradio/raw/main/test/test_files/video_sample.mp4",	# str (filepath or URL to file)
								#in 'parameter_16' Video component
				json,	# str (filepath to JSON file)
							#	in 'NExT-GPT Chatbot' Chatbot component
				0,	# int | float (numeric value between 0 and 1)
								#in 'Top P' Slider component
				0,	# int | float (numeric value between 0 and 1)
								#in 'Temperature' Slider component
				1,	# int | float (numeric value between 1 and 10)
								#in 'Guidance scale' Slider component
				10,	# int | float (numeric value between 10 and 50)
								#in 'Number of inference steps' Slider component
				1,	# int | float (numeric value between 1 and 10)
								#in 'Guidance scale' Slider component
				10,	# int | float (numeric value between 10 and 50)
								#in 'Number of inference steps' Slider component
				16,	# int | float (numeric value between 16 and 32)
								#in 'Number of frames' Slider component
				1,	# int | float (numeric value between 1 and 10)
								#in 'Guidance scale' Slider component
				10,	# int | float (numeric value between 10 and 50)
								#in 'Number of inference steps' Slider component
				1,	# int | float (numeric value between 1 and 9)
								#in 'The audio length in seconds' Slider component
				fn_index=0
)


# result = client.predict(
# 				"Hello!",	# str in 'Text' Textbox component
# 				None,	# str (filepath or URL to image)
# 							#	in 'Image' Image component
# 				None,	# str (filepath or URL to file)
# 							#	in 'parameter_14' Audio component
# 				None,	# str (filepath or URL to file)
# 							#	in 'parameter_16' Video component
# 				json,	# str (filepath to JSON file)
# 							#	in 'NExT-GPT Chatbot' Chatbot component
# 				0,	# int | float (numeric value between 0 and 1)
# 							#	in 'Top P' Slider component
# 				0,	# int | float (numeric value between 0 and 1)
# 							#	in 'Temperature' Slider component
# 				1,	# int | float (numeric value between 1 and 10)
# 							#	in 'Guidance scale' Slider component
# 				10,	# int | float (numeric value between 10 and 50)
# 							#	in 'Number of inference steps' Slider component
# 				1,	# int | float (numeric value between 1 and 10)
# 							#	in 'Guidance scale' Slider component
# 				10,	# int | float (numeric value between 10 and 50)
# 							#	in 'Number of inference steps' Slider component
# 				16,	# int | float (numeric value between 16 and 32)
# 							#	in 'Number of frames' Slider component
# 				1,	# int | float (numeric value between 1 and 10)
# 							#	in 'Guidance scale' Slider component
# 				10,	# int | float (numeric value between 10 and 50)
# 							#	in 'Number of inference steps' Slider component
# 				1,	# int | float (numeric value between 1 and 9)
# 							#	in 'The audio length in seconds' Slider component
# 				fn_index=1
# )


print(result)