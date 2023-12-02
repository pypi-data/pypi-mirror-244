from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from huscy.projects.models import Project


class EthicsCommittee(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = 'name',
        verbose_name = _('Ethics committee')
        verbose_name_plural = _('Ethics committees')


class Ethics(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ethics',
                                verbose_name=_('Project'))
    ethics_committee = models.ForeignKey(EthicsCommittee, on_delete=models.PROTECT,
                                         verbose_name=_('Ethics committee'))
    code = models.CharField(_('Code'), max_length=255, blank=True, default='')

    class Meta:
        ordering = '-project', 'ethics_committee__name'
        unique_together = 'project', 'ethics_committee'
        verbose_name = _('Ethics')
        verbose_name_plural = _('Ethics')


class EthicsFile(models.Model):
    class TYPE(models.IntegerChoices):
        proposal = 0, _('Proposal')
        votum = 1, _('Attachment')
        amendment = 2, _('Vote')
        cover_letter = 3, _('Cover letter')

    def get_upload_path(self, filename):
        project = self.ethics.project
        return f'projects/{project.id}/ethics/{filename}'

    ethics = models.ForeignKey(Ethics, on_delete=models.CASCADE, related_name='ethics_files',
                               editable=False, verbose_name=_('Ethics'))

    filetype = models.PositiveSmallIntegerField(_('File type'), choices=TYPE.choices)

    filehandle = models.FileField(_('File handle'), upload_to=get_upload_path, max_length=255,
                                  validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    filename = models.CharField(_('File name'), max_length=255)

    uploaded_at = models.DateTimeField(_('Uploaded at'), auto_now_add=True, editable=False)
    uploaded_by = models.CharField(_('Uploaded by'), max_length=126, editable=False)

    class Meta:
        ordering = '-ethics__project', '-ethics', 'filename'
        verbose_name = _('Ethic file')
        verbose_name_plural = _('Ethic files')
