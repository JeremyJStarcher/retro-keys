# Load ordered source files for compiling the finished lib
src_files = lib/variables.scad \
						lib/utilities.scad \
						lib/circuits/helpers.scad \
						lib/circuits/trrs.scad \
						lib/circuits/pro_micro.scad \
						lib/circuits/proton_c.scad \
						lib/circuits/ec11.scad \
						lib/circuits/mts_101.scad \
						lib/circuits/wire.scad \
						lib/circuits/trace.scad \
						lib/circuits/support.scad \
						lib/circuits.scad \
						lib/case.scad \
						lib/switches/stabilizers.scad \
						lib/switches/footprints.scad \
						lib/switches/rgb.scad \
						lib/switches/base.scad \
						lib/switches/mx.scad \
						lib/switches/choc_v1.scad \
						lib/switches.scad \
						keyboard.scad

git_tag = $(shell git describe --tags)
compiled_lib_name = keyboard_lib.${git_tag}.scad
tmp = tmp

regenerate = false

# Vars used for releasing
package_registry_url=${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/generic/scad_keyboard_lib/${git_tag}
changelog_url=${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/repository/changelog
changelog_anchor=$(shell echo ${git_tag} | sed 's,\.,,g')-$(shell date +"%Y-%m-%d")
changelog_link=${CI_PROJECT_URL}/-/blob/main/CHANGELOG.md\#${changelog_anchor}

ifndef CI_PROJECT_URL
override CI_PROJECT_URL = https://gitlab.com/alexives/keyboard_lib
endif

# This is the description used in the release item post
define release_description
### Changes

For changes, take a look at the [changelog entry for ${git_tag}](${changelog_link}).

### Update Instructions

#### For Submodule Installations
In the submodule directory, run `git checkout ${git_tag}`.
Then, check in the updated submodule.

#### For File Installations
Download [version ${git_tag}](${package_registry_url}/${compiled_lib_name}) (GitLab
requires you to be signed in to download the package) and replace the copy you use now.
Then update references to `use <${compiled_lib_name}>`
endef

test.nodeps:
	@touch /dev/null

build: ${src_files}
	@echo "// Keyboard Lib for OpenSCAD" > ${compiled_lib_name}
	@echo "// For more usage and information, see https://gitlab.com/alexives/keyboard_lib" >> ${compiled_lib_name}
	@echo >> ${compiled_lib_name}
	@echo "// Licensed Under:" >> ${compiled_lib_name}
	@sed -e 's,^,// ,g' LICENSE.md >> ${compiled_lib_name}
	@echo >> ${compiled_lib_name}
	@echo "// Usage" >> ${compiled_lib_name}
	@sed '/## Modules/,/# Development/!d;/# Development/q' Readme.md | sed -e 's,^,// ,g' | sed 's/# Development//' >> ${compiled_lib_name}
	@echo >> ${compiled_lib_name}
	@for f in $^; do \
		echo "\n\n// ${CI_PROJECT_URL}/-/blob/main/$$f" >> ${compiled_lib_name}; \
		sed -e "s/include.*//g" -e 's/use.*//g' $$f >> ${compiled_lib_name}; \
	done
	@echo "\nFinished building ${compiled_lib_name}\n"

specs/%_spec.scad: test.nodeps
	bin/openspecad $@

test:
	./bin/openspecad

test.ci:
	./bin/openspecad --gitlab-parallel

sca2d:
	sca2d --gitlab-report .

export release_description
release.description:
	@echo "$$release_description" > description.txt

clean:
	rm -f keyboard_lib.*.scad

# This only works in CI
release: build release.description
		curl --header "JOB-TOKEN: ${CI_JOB_TOKEN}" --upload-file ${compiled_lib_name} "${package_registry_url}/${compiled_lib_name}"
		curl --header "PRIVATE-TOKEN: ${CHANGELOG_TOKEN}" --data "version=${CI_COMMIT_TAG}" ${changelog_url}
		release-cli create --name "Release ${CI_COMMIT_TAG}" --tag-name ${CI_COMMIT_TAG} \
			--assets-link "{\"name\":\"${compiled_lib_name}\",\"url\":\"${package_registry_url}/${compiled_lib_name}\"}" \
			--description description.txt
