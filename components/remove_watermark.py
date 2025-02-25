def remove_watermark(
    pvc_directory    : str,
    pvc_filename     : str,
    remove_watermark : bool
):
    """
    Removes the watermark from the pdf file.

    Parameters:
        - pvc_directory (str) : The PVC directory where the file is saved.
        - pvc_filename  (str) : The PVC filename in which the watermark will be removed.
    """

    import fitz
    import os

    pvc_filename        = os.path.join(pvc_directory, pvc_filename)
    pvc_filename_output = '{0}_no_watermark{1}'.format(*os.path.splitext(pvc_filename))

    document = fitz.open(pvc_filename)

    if not remove_watermark:

        document.save(pvc_filename_output)
        return

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

    document.save(pvc_filename_output)


if __name__ == '__main__':
    """
    Elyra Pipelines
    """

    import os

    remove_watermark(
        pvc_directory    = os.getenv('pvc_directory'),
        pvc_filename     = os.getenv('pvc_filename'),
        remove_watermark = os.getenv('remove_watermark')
    )
