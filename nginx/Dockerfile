# syntax=docker/dockerfile:1
FROM nginx:latest
ARG run_as
ENV run_as=${run_as}
RUN adduser $run_as
WORKDIR /app
COPY ./monda_live.conf /etc/nginx/conf.d/default.conf
# RUN chown -R $run_as:$run_as /app && \
#         chown -R $run_as:$run_as /var/cache/nginx && \
#         chown -R $run_as:$run_as /var/log/nginx && \
#         chown -R $run_as:$run_as /etc/nginx/conf.d
# RUN touch /var/run/nginx.pid && \
#         chown -R $run_as:$run_as /var/run/nginx.pid
