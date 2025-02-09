#!/usr/bin/perl

# recfg - recreate Zone Config from zoneshow output

# This script builds a list of alicreate, zonecreate, and cfgadd
# commands, and then store these into a file. The
# outputfile(inputfile_new) then can be used to copy/paste the commands
# at the switch-shell.
#
# NOTES:
# - alias members are expected to be WWPNs only
# - zone members are expected to be aliasnames only
# - future release may test for WWPN/aliasname
#
# Follow-up steps can easily be performed using webtools:
# - create a new Zone Config
# - move all (or part) of the newly defined zones to the zone config
# - save/enable the config
#
# -------------------------------------------------------------------------------


use strict;
use warnings;
use Getopt::Long;
use Data::Dumper;

# Get commandline options
#
my %Options=();

GetOptions (
            \%Options,
            'prefix=s'         => \$Options{'prefix'},
            'postfix=s'        => \$Options{'postfix'},
            'rmlsan'           => \$Options{'rmlsan'},
            'debug|d'          => \$Options{'debug'},
            'help|h'           => \$Options{'help'}
);

my $usage='

    recfg [-prefix string] [-postfix string] [-rmlsan] [-debug] [-help] <source_cfgshow_inputfile> [target_activeZoneSetName]

    source_cfgshow_inputfile     textfile created using cfgshow command
                                 minimally contains Defined Configuration details

    OPTIONS
            prefix        put string in front of alias names and zonenames
            postfix       put string at end of alias names and zonenames
            rmlsan        remove LSAN_ from routed zone names
            debug         provide debug output
            help          print this usage information

    NOTE
    prefix and/or postfix strings may help in creating unique names when merging (routed) SANs

    EXAMPLE:
    # remexec -v -l recc1 "ssh admin@pnj-sansw149 cfgshow" > pnj-sansw149_cfgshow
    # recfg pnj-sansw149_cfgshow  pnj_sasnw501

';

if ($Options{'help'}) { print $usage; exit }

my ($inputfile,$activezonesetname,$rest) = @ARGV;

die "No inputfile given!\n$usage"                 if (not defined $inputfile);

#die "No outputfile given!\n$usage"                if (not defined $outputfile);
die "Too many commandline arguments!\n$usage"     if (defined $rest);


# Initialize variables
#
my ($IF,$OF)=();
my (@ALIAS,@ZONE,@T)=();
my $switch=0;        # 0=no zone/alias; 1=alias; 2=zone
my $name="";
my $regel="";
my $prefix="";
my $postfix="";
my $line=0;
my $matchline=0;
my (%aliasH, %zoneH,%aZone) =();
my $outputfile = $inputfile . "_" . "recreate_zones";

$activezonesetname="active_zoneset_name" if (not defined $activezonesetname);

open($IF, '<', $inputfile)  or die "Could not open file '$inputfile\n$usage' $!";
open($OF, '>', $outputfile) or die "Could not open file '$outputfile\n$usage' $!";

$prefix=$Options{'prefix'}   if ($Options{'prefix'});
$postfix=$Options{'postfix'} if ($Options{'postfix'});

while (<$IF>) {

    chomp;
    s/\r\n|\n|\r/\r\n/g;      # convert to DOS style textfile (
    s/^M//g;                  # delete any ^M character
    s/^\s+//;                 # delete leading whitespace
    s/\s+$//;                 # delete trailing whitespace

    ## generate active zone hash
    #last if (/Effective configuration/i);       # skip lines to the end
    ++$line;
    if (/Effective configuration/io) {           # process lines after the match
        $matchline = $line;
    }

    if ($matchline > 0) {
        ## loop to create zonehash pair
        if (/zone:/) {
            $switch=3;
            $regel="";

            @T=split /\s+/;
            $name=$T[-1];
            $regel=$name;
            next;
        }
        push @{$aZone{$regel}}, $_ if ( (/^\d\d:/) && ($switch==3) );
        next;

        #$switch = 0;      # reset $switch
    }
    ## end of active zone hash


    if (/alias:/) {
        $switch=1;
        $regel="";

        @T=split /\s+/;
        $name=$T[-1];

        $regel=sprintf "%s %s%s%s, '", "alicreate", $prefix, $name, $postfix;
        next;
    }

    if (/zone:/) {
        $switch=2;
        $regel="";

        @T=split /\s+/;
        $name=$T[-1];

        $name =~ s/LSAN_//
          if ($Options{rmlsan});    # remove LSAN_ from zonenames
        $regel=sprintf "%s %s%s%s, '", "zonecreate", $prefix, $name, $postfix;
        next;
    }

    if ($switch) {

   # if line ends with an apostrophe then there will be a next line with member details
   # if line doesn't end with an apostrophe then it is the last line with member details
   # so the completed alias or zone command can be pushed to the array
   #

        if (/\;$/) {
            s/(\S+)([;])/$prefix$1$2/g
              if ( ($prefix)  && ($switch == 2) );      # add prefix to zonemembers
            s/(\S+)([;])/$1$postfix$2/g
              if ( ($postfix) && ($switch == 2) );      # add postfix to zonemembers
            $regel=sprintf "%s%s ", $regel, $_;
            next;
        } else {
            s/(\S+)([;])/$prefix$1$2/g
              if ( ($prefix)  && ($switch == 2) );      # add prefix to zonemembers
            s/(\S+)([;])/$1$postfix$2/g
              if ( ($postfix) && ($switch == 2) );      # add postfix to zonemembers
            s/(\S+)$/$1$postfix/g
              if ( ($postfix) && ($switch == 2) );      # add postfix to zonemembers

            #print $switch . " ". $_ . "\n";           ## print wwpn
            $aliasH{$name} = $_ if ($switch == 1);     ## create alias hash
            $zoneH{$name} = $_ if ($switch == 2);      ## create alias hash

            $regel=sprintf "%s%s'", $regel, $_;

            push (@ALIAS, $regel) if ($switch == 1);
            push (@ZONE,  $regel) if ($switch == 2);

            $switch=0;      # reset $switch
            next;
        }
    }
}

#print Dumper(\%aZone);
#print Dumper(\%zoneH);
#print Dumper(\%aliasH);
#print Dumper(\@ALIAS);
print "number of zones configed does not match number in active zoneset \n"
  if (scalar(@ZONE) != scalar(keys %aZone));

sub a2h(@) {
    my %z2h;
    foreach my $v (@_) {
        $v =~ s/zonecreate |alicreate //g;
        $v =~ s/\'//g;
        $v =~ s/ //g;
        my ($key, $val) = split(/,/, $v);
        $z2h{$key} = $val;
    }
    return %z2h;
}

# Create outputfile
#

foreach (sort @ALIAS) {
    printf "ALIAS: %s\n", $_ if ($Options{'debug'});
    printf $OF "%s\n", $_;
}

foreach (sort @ZONE) {
    printf "ZONE:  %s\n", $_ if ($Options{'debug'});
    printf $OF "%s\n", $_;
}

foreach (sort keys %aZone) {
    printf $OF "cfgadd $activezonesetname,%s\n", $_;

    #printf $OF "%s\n", $_;
}

close ($OF);
print "\nDone: $outputfile created. \n\n";
