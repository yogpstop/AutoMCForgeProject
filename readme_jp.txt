�g�p���@
1.build.cfg���v���W�F�N�g�t�H���_�ɍ쐬���A�K�v�ɉ����Ĉȉ��̍��ڂ��L�q����
��1����1�s
�K�{����
    1.�t�@�C���擪��"[pj]"�ƋL�q����B
    2.�\�[�X�R�[�h�̓������f�B���N�g����"src="�ɑ����ċL�q����B(��1,2,3,4)
    3."version="�ɑ����āAMod�̃o�[�W�������L�q����B
�C�ӎ���
    4.���\�[�X���[�߂Ă���f�B���N�g���������"res="�ɑ����ċL�q����B(��1,2,3,4)
    5.����MOD�̃r���h��API���K�v�Ȃ�K�v��API�̖��O��"api="�ɑ����ċL�q����B(��1,2,5)
    6.����MOD��API�Ƃ��ďo�͂�������Ώo�͂�����API�̖��O��"capif="�ɑ����ċL�q����B(��1,6)
    7.�\�[�X�R�[�h�y�у��\�[�X�t�@�C���̒��ŏ����������������񂪂���΁A"rep="�ɑ����ċL�q����B(��7)
    8.�o�̓t�@�C�����y�яꏊ���w�肵�������"out="�ɑ����ċL�q����B(��1,3,9)
    9.(�񐄏�)Minecraft�̃o�[�W�������蓮�Ŏw�肵�������"mcv="�ɑ����ċL�q����B(��8)
��
    1.�f�B���N�g���̕���������"/"�ł���
        ex)"dir"�t�H���_����"ff"�t�H���_���w�肷��ꍇ�́A"dir/ff"
    2.�����̍��ڂ��w�肷��ۂ�":"�ŋ�؂�(=Windows���Ɛ�΃p�X�̎w��͕s�\)
        ex)"a"�t�H���_��"b"�t�H���_��"c/d"�t�H���_���w�肷��ꍇ�́A"a:b:c/d"
    3.�v���W�F�N�g�t�H���_����̑��΃p�X�Ŏw�肷��
        ex)"�v���W�F�N�g�t�H���_/a/b/c"�́A"a/b/c"
    4.������"/"������ꍇ�́A���̃t�H���_�̒��g���R�s�[����B�Ȃ��ꍇ�͂��̃t�H���_���ƃR�s�[����
        ex)"src"�Ǝw�肵���ꍇ�A����t�H���_��"src"�t�H���_�����������B
        ex)"src/"�Ǝw�肵���ꍇ�A����t�H���_�����ɁA"src"�̒��g���R�s�[�����B
    5.�C�ӎ���6�Ŏw�肵�����O�Ɉ�v������
        ex)"capif=TestCraft"�Ǝw�肵�ďo�͂���API���g��������΁A"api=TestCraft"�Ǝw�肷��B
    6.�����ŕK�v�ȏꏊ�ɕۑ������̂ŁA�����ŃR�s�[�����肵�Ȃ��Ă悢
        ex)"capif=TestCraft"�Ǝw�肵�Ĉ�xBuild����Εʂ̃v���W�F�N�g����API�Ƃ��Ďg�p�o����B
    7.�e���ڂ�"|"�ŕ������A�ϊ��O�ƕϊ���̕������"="�ŋ�؂�
        ex)"@TEST@"��"flower"�ɁA"#TEST#"��"rose"�ɕϊ���������΁A"@TEST@=flower|#TEST#=rose"�Ǝw�肷��B
    8.eclipse�̃v���W�F�N�g���Z�b�g�A�b�v����ۂɎ����œ��͂����̂ŁA�蓮�ł̐ݒ�͔񐄏�
        ex)update eclipse project file�����s����΁A������mcv�̃I�v�V�����̓��e���w�肳���B
    9.�f�t�H���g�ł́A"�v���W�F�N�g�t�H���_/dist/(Minecraft�̃o�[�W����)/(�v���W�F�N�g��)-(MOD�̃o�[�W����).zip"�ɏo�͂����B
�Ȃ��A�ǂ̍��ڂ��]���ȃX�y�[�X�������Ă���ƃG���[���o�邽�ߒ��ӂ��邱�ƁB
2.�����|�W�g���̒��g���A�v���W�F�N�g�t�H���_��1��(���[�N�X�y�[�X�t�H���_)�ɑS�ăR�s�[����B(.git�͕s�v)
3.boot.bat��boot.sh���N������B
4.����N�����͎�����forge�̃C���X�g�[�����n�܂邽�߁A�w���ɏ]����Minecraft��Forge�̃o�[�W�������w�肷��B
5.(����N������Forge�C���X�g�[�����I��莟��)���j���[���\������邽�߁A�s���������Ƃ�I�ԁB
    '0. exit'
        �X�N���v�g���I������
    '1. build project (an project chosen by user) *current minecraft version is unavailable'
        ���̉�ʂőI������1�̃v���W�F�N�g���r���h����B(���ڂ̌�ɏo�Ă�Minecraft�̃o�[�W�����͖���(build.cfg�ɋL�q���ꂽ�o�[�W�������g�p�����))
    '2. update eclipse project file (all projects)'
        build.cfg�����݂���v���W�F�N�g�t�H���_�S�ĂɁA���ݑI�𒆂̃o�[�W������Forge�ɍ��킹��eclipse�v���W�F�N�g���C���X�g�[������B
    '3. update eclipse project file (some projects chosen by user)'
        build.cfg�����݂���v���W�F�N�g�t�H���_�̒��ŁA���[�U�[���I�񂾕����̃t�H���_�Ɍ��ݑI�𒆂̃o�[�W������Forge�ɍ��킹��eclipse�v���W�F�N�g���C���X�g�[������B
    '4. update eclipse project file (an project chosen by user)'
        build.cfg�����݂���v���W�F�N�g�t�H���_�̒��ŁA���[�U�[���I��1�̃t�H���_�Ɍ��ݑI�𒆂̃o�[�W������Forge�ɍ��킹��eclipse�v���W�F�N�g���C���X�g�[������B
    '5. install new minecraft forge'
        �V����Forge���C���X�g�[������B(1��Minecraft�̃o�[�W�����ɑ΂���1��Forge�������݂ł��Ȃ��B���̂��߁A���łɂ���Minecraft�̃o�[�W������I������ƁA�㏑�������B)
    '6. change minecraft version'
        ���ݑI�𒆂�Minecraft�o�[�W������ύX����B
6.��{�I�ɑI����ʂł́A��Ɍ�₪�o��̂ł��̒�����Y��������̂�I�����Ă����B