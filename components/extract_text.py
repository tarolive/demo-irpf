def extract_text(
    pvc_directory : str,
    pvc_filename  : str
):
    """
    Extracts the text from the pdf file.

    Parameters:
        - pvc_directory (str) : The PVC directory where the file is saved.
        - pvc_filename  (str) : The PVC filename in which the text will be extracted.
    """

    import os
    import pandas
    import pdf2image
    import pytesseract

    pvc_filename = os.path.join(pvc_directory, pvc_filename)
    pvc_filename = '{0}_no_watermark{1}'.format(*os.path.splitext(pvc_filename))

    extracted_text = ''

    for index, image in enumerate(pdf2image.convert_from_path(pvc_filename)):

        ocr_config           = r'-c preserve_interword_spaces=1 --oem 1 --psm 1'
        ocr_data             = pytesseract.image_to_data(image, lang = 'por', config = ocr_config, output_type = pytesseract.Output.DICT)
        ocr_dataframe        = pandas.DataFrame(ocr_data)
        cleaned_df           = ocr_dataframe[(ocr_dataframe.conf != '-1') & (ocr_dataframe.text != ' ') & (ocr_dataframe.text != '')]
        sorted_block_numbers = cleaned_df.groupby('block_num').first().sort_values('top').index.tolist()

        for block_num in sorted_block_numbers:

            current_block  = cleaned_df[cleaned_df['block_num'] == block_num]
            filtered_text  = current_block[current_block.text.str.len() > 3]
            avg_char_width = (filtered_text.width / filtered_text.text.str.len()).mean()

            prev_paragraph, prev_line, prev_left_margin = 0, 0, 0

            for idx, line_data in current_block.iterrows():

                if prev_paragraph != line_data['par_num']:
                    extracted_text   += '\n'
                    prev_paragraph   = line_data['par_num']
                    prev_line        = line_data['line_num']
                    prev_left_margin = 0

                elif prev_line != line_data['line_num']:
                    extracted_text   += '\n'
                    prev_line        = line_data['line_num']
                    prev_left_margin = 0

                spaces_to_add = 0

                if line_data['left'] / avg_char_width > prev_left_margin + 1:

                    spaces_to_add  = int((line_data['left']) / avg_char_width) - prev_left_margin
                    extracted_text += ' ' * spaces_to_add

                extracted_text   += line_data['text'] + ' '
                prev_left_margin += len(line_data['text']) + spaces_to_add + 1

            extracted_text += '\n'

    print(f'extracted_text : {extracted_text}')

    with open(pvc_filename.replace('.pdf', '.txt'), 'w') as file:

        file.write(extracted_text)


if __name__ == '__main__':
    """
    Elyra Pipelines
    """

    import os

    extract_text(
        pvc_directory = os.getenv('pvc_directory'),
        pvc_filename  = os.getenv('pvc_filename')
    )
