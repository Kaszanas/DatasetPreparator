## 2.0.0 (2025-03-08)

### Feat

- **sc2_map_downloader**: using SC2InfoExtractor go, adjusted documentation
- **sc2egset_pipeline**: tested full processing pipeline manually
- **directory_packager**: multithreading in directory packager
- **directory_flattener**: multithreading file copying
- added new replaypacks to available_replaypacks
- added sc2egset_pipeline to dockerfiles
- separate sc2egset_pipeline and replaypack_processor
- ignoring maps directory
- (directory_packager.py) added tqdm progres bar
- drafted full SC2ReSet/SC2EGSet pipeline
- **json_merger.py**: added user prompting, and CLI flag
- added force_overwrite flag to CLI
- **directory_packager.py**: added user prompting
- **directory_flattener.py**: added user_prompt feature
- drafted utils/user_prompt
- draft functionality of sc2egset_replaypack... full pipeline
- added processed_mapping_copier target to makefile
- test workspace in .env
- sc2infoextractorgo executable path in settings
- added default flag values for golang
- added directory checks before file_renamer
- retry functionality for download_replaypack
- split download_file from download_replaypack
- md5 checksum verification for downloaded replaypacks
- added md5 checksums to available replaypacks

### Fix

- **docker**: fixing volume mount for CI
- **directory_flattener**: returning list of processed directories
- fixing file_renamer using directory name
- fixing replaypack_processor, no exceptions
- using Path as the inferred path type
- fixing non-existent argument
- **sc2_replaypack_processor**: fixing maps directory as arg
- continue instead of break after download
- **directory_flattener.py**: manually tested flattening directories
- manually tested directory_packager, working version
- fixing pre-commit in dev docker
- fixing return value, removed range loop
- fixing opening and writing to file
- fixing imports in sc2reset
- mounting curdir as a dot
- fixing paths in Dockerfile
- converting paths with click, changed target name
- fixing glob issues, testing directory flattener
- fixed log level, fixing path initialization
- pointing CLA to main
- fixed import issues in replaypack downloader
- getting list of files instead of generator
- fixed missing argument in json_merger
- lowercase makefile name
- added logs directory
- different retry logic, using path to merge suffix
- changed commitizen pre-commit config
- removed commitizen-branch hook
- **deps**: pre-commit autoupdate
- **deps**: added commitizen to pre-commit

### Refactor

- **directory_flattener**: renamed n_processes -> n_threads
- removing unused code, replaypack processor
- maps directory is created, skipping check
- removed unused code
- force_overwrite continues directory flattning
- command saved to a variable
- removed old directory structure from processing
- added logging statements
- applied user prompting for every script
- **processed_mapping_copier.py**: using pathlib, refactored functionality with iterdir
- renamed force to force_overwrite
- using glob instead of os.walk
- **user_prompt.py**: added logging
- applied user prompting in sc2egset_replaypack_processor
- renamed user prompting function
- drafting refactor of sc2egset_replaypack_processor
- using dev dockerfile in sc2reset_sc2egset process
- adjusted make targets for sc2egset, removed unused param
- changed the processing dir structure
- refreshed ci installing poetry
- renamed dir_packager to directory_packager
- capitalized "AS" in docker
- renamed sc2_replaypack_processor -> sc2egset_replaypack
- multiprocessing off in sc2_replaypack_processor
- no random uuid, using file hash in flattener
- using new argument classes, refactor
- added utils directory, drafted README
- fixed end of file in cla.json
- sync commit
- changed dir_flattener logic, using a list of files
- deleted legacy setup.py
- ran pre-commit on all files

### Perf

- directory_flattener, hash from filepath, added tqdm
- downloading maps as a pre-process step

## 1.2.0 (2022-06-08)

## 1.1.0 (2022-03-17)

## 1.0.0 (2021-08-27)
