#!/bin/sh

. ../_env.sh

# Retrieve data
$docker_cmd $ruby_docker_image sh -c "ruby get_all_list.rb"
