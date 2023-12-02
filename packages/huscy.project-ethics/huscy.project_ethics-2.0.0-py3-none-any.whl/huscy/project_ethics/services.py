from huscy.project_ethics.models import Ethics, EthicsCommittee, EthicsFile


def create_ethics_committee(name):
    return EthicsCommittee.objects.create(name=name)


def get_ethics_committees():
    return EthicsCommittee.objects.all()


def update_ethics_committee(ethics_committee, name):
    ethics_committee.name = name
    ethics_committee.save(update_fields=['name'])
    return ethics_committee


def create_ethics(project, ethics_committee, code=''):
    return Ethics.objects.create(project=project, ethics_committee=ethics_committee, code=code)


def get_ethics(project):
    return Ethics.objects.filter(project=project)


def update_ethics(ethics, ethics_committee, code):
    ethics.code = code
    ethics.ethics_committee = ethics_committee
    ethics.save()
    return ethics


def create_ethics_file(ethics, filehandle, filetype, creator, filename=''):
    filename = filename or filehandle.name.split('/')[-1]

    return EthicsFile.objects.create(
        ethics=ethics,
        filehandle=filehandle,
        filename=filename,
        filetype=filetype,
        uploaded_by=creator.get_full_name(),
    )


def get_ethics_files(ethics):
    return EthicsFile.objects.filter(ethics=ethics)


def update_ethics_file(ethics_file, filetype, filename):
    ethics_file.filetype = filetype
    ethics_file.filename = filename
    ethics_file.save()
    return ethics_file
