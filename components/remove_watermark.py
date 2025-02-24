def remove_watermark(
    pvc_directory : str,
    pvc_file      : str
):
    """
    Removes the watermark from the pdf file.

    Parameters:
        - pvc_directory (str) : The PVC directory where the file is saved.
        - pvc_file      (str) : The PVC pdf file to remove the watermark.
    """

    import fitz
    import os

    document = fitz.open(os.path.join(pvc_directory, pvc_file))

    for page in document:

        images = page.get_images(full = True)

        for image in images:

            page.delete_image(image[0])

        annots = page.annots()

        if annots:

            for annot in annots:

                if 'Watermark' in annot.info.get('title', ''):

                    annot.set_Flags(fitz.ANNOT_HIDDEN)

        page.apply_redactions()

    document.save(pvc_directory)


if __name__ == '__main__':
    """
    Elyra Pipelines
    """

    import os

    remove_watermark(
        pvc_directory = os.getenv('pvc_directory'),
        pvc_file      = os.getenv('pvc_file')
    )
