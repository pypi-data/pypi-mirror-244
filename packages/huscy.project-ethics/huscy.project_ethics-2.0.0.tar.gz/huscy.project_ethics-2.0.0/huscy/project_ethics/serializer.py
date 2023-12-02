from rest_framework import serializers

from huscy.project_ethics import models, services


class EthicsCommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EthicsCommittee
        fields = 'id', 'name'

    def create(self, validated_data):
        return services.create_ethics_committee(**validated_data)

    def update(self, ethics_committee, validated_data):
        return services.update_ethics_committee(ethics_committee, **validated_data)


class EthicsFileSerializer(serializers.ModelSerializer):
    filename = serializers.CharField(required=False, default='')
    filetype_name = serializers.CharField(source='get_filetype_display', read_only=True)

    class Meta:
        model = models.EthicsFile
        fields = (
            'id',
            'ethics',
            'filehandle',
            'filename',
            'filetype',
            'filetype_name',
            'uploaded_at',
            'uploaded_by',
        )

    def create(self, validated_data):
        return services.create_ethics_file(**validated_data)


class UpdateEthicsFileSerializer(serializers.ModelSerializer):
    filetype_name = serializers.CharField(source='get_filetype_display', read_only=True)

    class Meta:
        model = models.EthicsFile
        fields = (
            'id',
            'ethics',
            'filehandle',
            'filename',
            'filetype',
            'filetype_name',
            'uploaded_at',
            'uploaded_by',
        )
        read_only_fields = 'filehandle',

    def update(self, ethics_file, validated_data):
        return services.update_ethics_file(ethics_file, **validated_data)


class EthicsSerializer(serializers.ModelSerializer):
    ethics_committee_name = serializers.CharField(source='ethics_committee.name', read_only=True)
    ethics_files = EthicsFileSerializer(many=True, read_only=True)

    class Meta:
        model = models.Ethics
        fields = (
            'id',
            'code',
            'ethics_committee',
            'ethics_committee_name',
            'ethics_files',
            'project',
        )
        read_only_fields = 'project',

    def create(self, validated_data):
        return services.create_ethics(**validated_data)

    def update(self, ethics, validated_data):
        return services.update_ethics(ethics, **validated_data)
