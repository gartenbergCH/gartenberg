FROM python:3.10
WORKDIR /opt
COPY ./gartenberg /opt/gartenberg
COPY ./manage.py /opt/manage.py
COPY ./requirements.txt /opt/requirements.txt

ARG juntagrico_username
ARG juntagrico_email
ARG juntagrico_password
ARG juntagrico_secret_key

RUN pip install --no-cache-dir -r requirements.txt \
	&& chmod +x manage.py \
	&& ./manage.py migrate \
	&& export DJANGO_SUPERUSER_PASSWORD=$juntagrico_password \
	&& ./manage.py createsuperuser --noinput --username $juntagrico_username --email $juntagrico_email \
	&& ./manage.py create_member_for_superusers \
	&& ./manage.py generate_testdata \
	&& ./manage.py collectstatic
ENV JUNTAGRICO_SECRET_KEY $juntagrico_secret_key
EXPOSE 8000
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
