from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.TextField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'users'


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.TextField(unique=True)
    name = models.TextField()
    code = models.TextField()
    sis_course_id = models.TextField(unique=True)
    contact_name = models.TextField()
    contact_email = models.TextField()
    hub_url = models.TextField()
    hub_token = models.TextField()
    welcome_email_sent = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courses'


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(unique=True)
    display = models.TextField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'roles'


class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    repo = models.TextField(unique=True)
    tag = models.TextField()
    name = models.TextField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'images'


class Deployment(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.TextField(unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    release = models.TextField()
    message = models.TextField()
    commit_sha = models.TextField()
    file_sha = models.TextField()
    public_manifest = models.TextField()
    secret_manifest = models.TextField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'deployments'


class Token(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    token = models.TextField(unique=True)
    expiry = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tokens'


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'user_courses'
        unique_together = (('user', 'course'),)


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'user_roles'
        unique_together = (('user', 'role'),)


class CourseSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, unique=True)
    image = models.ForeignKey(Image, on_delete=models.DO_NOTHING)
    storage_capacity = models.TextField()
    cpu_request = models.TextField()
    cpu_limit = models.TextField()
    memory_request = models.TextField()
    memory_limit = models.TextField()
    lab_ui = models.BooleanField()
    placeholder_count = models.IntegerField()
    cull_time = models.IntegerField()
    spawner = models.TextField()
    image_puller_enabled = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'course_settings'


class CourseExtraEnv(models.Model):
    id = models.BigAutoField(primary_key=True)
    course_settings = models.ForeignKey(CourseSettings,
                                        on_delete=models.CASCADE)
    key = models.TextField()
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'course_extra_envs'
        unique_together = (('course_settings', 'key'),)


class CourseGitPullerTarget(models.Model):
    id = models.BigAutoField(primary_key=True)
    course_settings = models.ForeignKey(CourseSettings,
                                        on_delete=models.CASCADE)
    key = models.TextField(unique=True)
    repo = models.TextField()
    branch = models.TextField()
    target_dir = models.TextField()

    class Meta:
        managed = False
        db_table = 'course_git_puller_targets'
