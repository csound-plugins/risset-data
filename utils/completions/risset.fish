# fish completions for risset
set -l commands list install remove show man update listopcodes

complete -f -c risset -l update -d 'Update rissets database before running any command'
complete -f -c risset -l debug -d 'Run command showing debugging information'
complete -f -c risset -l repopath -d "Use this path to read data instead of the default path"

complete -f -c risset -n "not __fish_seen_subcommand_from $commands" -a install -d 'Install a package'
complete -f -c risset -n "not __fish_seen_subcommand_from $commands" -a list -d 'List available packages'
complete -f -c risset -n "not __fish_seen_subcommand_from $commands" -a show -d 'Show information about a package'
complete -f -c risset -n "not __fish_seen_subcommand_from $commands" -a man -d 'Open manual page for an opcode'
complete -f -c risset -n "not __fish_seen_subcommand_from $commands" -a update -d 'Update rissets data repository'
complete -f -c risset -n "not __fish_seen_subcommand_from $commands" -a remove -d 'Remove a package'
complete -f -c risset -n "not __fish_seen_subcommand_from $commands" -a listopcodes -d 'List installed opcodes'
complete -f -c risset -n "not __fish_seen_subcommand_from $commands" -a resetcache -d 'Remove local clones'



complete -f -c risset -n "__fish_seen_subcommand_from man" -a "(risset listopcodes)"
complete -f -c risset -n "__fish_seen_subcommand_from install" -a "(risset list --notinstalled --nameonly)"
complete -f -c risset -n "__fish_seen_subcommand_from remove" -a "(risset list --installed --nameonly)"
complete -f -c risset -n "__fish_seen_subcommand_from show" -a "(risset list --nameonly)"
