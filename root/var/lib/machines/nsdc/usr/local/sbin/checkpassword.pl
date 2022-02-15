#!/usr/bin/perl
# This Script will check password complexity
# Got this script from https://www.mylinuxplace.com/tag/check-password-script/ and adapted it to work...

use strict;

my $min_length;
my $min_uppercase;
my $min_lowercase;
my $min_digits;
my $min_specialchar;
my $reason;

# get the password from standard input ( possible to pipe )
my $str_pass=<STDIN>;

# Check if password policy flag file exists
if (-e "/srv/password-policy-none") {
        $min_length=7;
        $min_uppercase=0;
        $min_lowercase=0;
        $min_digits=0;
        $min_specialchar=0;
} else {
        $min_length=7;
        $min_uppercase=1;
        $min_lowercase=1;
        $min_digits=1;
        $min_specialchar=1;
}

# now lets start check and update the counters is we find something
# but first lets set all counters to zero
my $ctr_length=0;
my $ctr_uppercase=0;
my $ctr_lowercase=0;
my $ctr_digits=0;
my $ctr_specialchar=0;
# conver the string to array
my @array_pass = split('',$str_pass);
foreach my $pass_char (@array_pass)
{
        $ctr_length++;
        # check uppercase
        if($pass_char =~ /[A-Z]/)
        {
                $ctr_uppercase++;
        }
	# check lowercase
        elsif($pass_char =~ /[a-z]/)
        {
                $ctr_lowercase++;
        }
	# check digits
        elsif($pass_char =~ /[0-9]/)
        {
                $ctr_digits++;
        }
	# check special chars
        elsif($pass_char =~ /[\W_]/)
        {
                $ctr_specialchar++;
        }
}
# check if we reached minimal length
if($ctr_length<$min_length)
{
        print "Too short, minimum $min_length and got $ctr_length \n";
        exit 3;
}
# check if we reached minimal UPPER case
if($ctr_uppercase<$min_uppercase)
{
        print "Not enough uppercase, minimum $min_uppercase and got $ctr_uppercase \n";
        exit 6;
}
# check if we reached minimal lower case
if($ctr_lowercase<$min_lowercase)
{
        print "Not enough lowercase, minimum $min_lowercase and got $ctr_lowercase \n";
        exit 7;
}
# check if we reached minimal digits
if($ctr_digits<$min_digits)
{
        print "Not enough digits, minimum $min_digits and got $ctr_digits \n";
        exit 5;
}
# check if we reached minimal special characters
if($ctr_specialchar<$min_specialchar)
{
        print "Not enough special characters, minimum $min_specialchar and got $ctr_specialchar \n";
        exit 8;
}

if (! -e "/srv/password-policy-none") {
        my $tmp = qx(echo -n '$str_pass' | /usr/sbin/cracklib-check);
        ($str_pass,$reason) = split(/:([^:]+)$/, $tmp); # split on last occurenct of colon
        $reason =~ s/^\s+//;
        $reason =~ s/\s+$//;
        if($reason !~ /OK/) {
                print "Cracklib: " . $reason . "\n";
                exit 4; #system error
        }
}

# if you got up to here , meaning you passed it all with success
# we can now return a non error exit
exit 0;
