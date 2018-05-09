#!/usr/bin/perl

%actors = ();
$usage="$0 bash_script\n";
%started = ();
%actions = ();
if ($#ARGV < 0)
{
    print $usage;
    exit 1;
}
$fh = new IO::File($ARGV[0]);
$ti = 0;
$trigger = "";
$event = "";
$emit = "";
$na = 0;
while(<$fh>)
{
    $_ =~ s/^\s+//;
    $_ =~ s/\s+$//;
    $actor = "";
    if ($_ =~ /^ssh/)
    {
	@items = split /\s+/, $_;
	shift(@items);
	for $i (@items)
	{
	    if ($i =~ /^\-/)
	    {
		shift(@items);
	    }
	    else
	    {
		if (!exists($actors{$i}))
		{
		    $actors{$i} = $na;
		    $na += 1;
		}
		$actor = $i;
		last;
	    }
	}
	if ($_ !~ /\&$/)
	{
	    $emit = "emit";
	}
	else
	{
	    $emit = "";
	}
	# Find the command
	my @chars = split("", $_);
	my $start = -1;
	my $end = -1;
	for($i=0; $i<$#chars; $i++) 
	{
	    if ($chars[$i] eq '"')
	    {
		$start = $i;
		last;
	    }
	}
	for($i=$#chars; $i>0; $i--) 
	{
	    if ($chars[$i] eq '"')
	    {
		$end = $i;
		last;
	    }
	}
	$cmd = substr($_, $start+1, $end-$start-1);
	@cmds = split /\;|\&\&/, $cmd;
	$action = "";
	for $cm (@cmds)
	{
	    #print "$cm\n";
	    # Drop sudo if it is there
	    $cm =~ s/sudo//;
	    # Drop spaces around the command
	    $cm =~ s/^\s+//;
	    $cm =~ s/\s+$//;

	    # This is what we want, would like to have
	    # just a path to script to but can add later
	    if ($cm =~ /^sh|^bash|^perl|^python/)
	    {
		#print "Action command $cm\n";
		@words = split /\s+/, $cm;
		$action = $words[1];
		@parts = split /\//, $action;
		$action = $parts[$#parts];
		# remember what was started with this interpreter
		push(@{$started{$words[0]}},$action);
		last;
	    }
	    elsif ($cm =~ /^sleep/)
	    {
		$trigger = "wait t" . $ti;
		$ti += 1;
	    }
	    elsif ($cm =~ /^kill |^pkill|^killall/)
	    {
		$killed = "";
		@words = split /\s+/, $cm;
		if ($cm =~ /^kill |^pkill/)
		{
		    $prog = $words[2];
		}
		else
		{
		    $prog = $words[1];
		}
		if(exists($started{$prog}))
		{
		    for $a (@{$started{$prog}})
		    {
			#print "Killing $a\n";
			if ($killed ne "")
			{
			    $killed .= ", ";
			}
			$killed .= $a;
		    }
		}
		if ($killed eq "")
		{
		    $killed = $prog;
		}
		# Drop path if any, but save for bindings
		@parts = split /\//, $killed;
		$killed = $parts[$#parts];
		$killed =~ s/^start\_//;
		$action = "stop_" . $killed;
		#print "Action $action\n";
		last;
	    }
	    elsif ($cm !~ "cd")
	    {
		@words = split /\s+/, $cm;
		@parts = split /\//, $words[0];
		$action = $parts[$#parts];
		last;
	    }
	}
	# Drop extension if any
	$action =~ s/\..*$//;
	if($action ne "")
	{
	    if ($event ne "")
	    {
		$temp = "when " . $event;
		if ($trigger ne "")
		{
		    $temp = $temp . " " . $trigger;
		}
		$trigger = $temp;
		$event = "";
	    }
	    if ($emit ne "")
	    {
		$event = $action . "_done";
	    }
	    if ($trigger ne "")
	    {
		print "$trigger ";
	    }
	    print "actor$actors{$actor} $action";
	    if ($emit ne "")
	    {
		print " $emit $event";
	    }
	    print "\n";

	    if ($trigger ne "")
	    {
		$trigger = "";
	    }
	    else
	    {
		$event = "";
	    }
	    $actions{$action} = $cmd;
	}
	
    }
    if ($_ =~ /^sleep/)
    {
	$trigger = "wait t" . $ti;
	$ti += 1;
    }
}
print "bindings:\n";
for $a (keys %actions)
{
    print "\t $a $actions{$a}\n";
}
