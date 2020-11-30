set fish_color_command red
set fish_color_param green
set fish_color_error brblue

function fish_prompt
	set machineName (cat /proc/sys/kernel/hostname)
	
	
	
	set cwd (string replace /home/$USER "~" $PWD)
	
	set sign ""
	if [ "$USER" = "root" ]
		set sign "# "
	else
		set sign '$ '
	end

	echo (set_color brmagenta)$machineName(set_color yellow)"@"(set_color brgreen)$USER(set_color white)": "(set_color red)$cwd(set_color green)"]"(set_color brblack)$sign
end