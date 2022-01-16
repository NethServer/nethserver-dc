#!/usr/bin/perl -w
# This Script will check password complexity
# Got this script from https://www.mylinuxplace.com/tag/check-password-script/ and adapted it to work...

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
$specialchars='!,@,$,#,%,^,&,*,(,),-,_,+,=';
# get the password from standard input ( possible to pipe )
$str_pass=<STDIN>;
# now lets start check and update the counters is we find something
# but first lets set all counters to zero
$ctr_length=-1;
$ctr_uppercase=0;
$ctr_lowercase=0;
$ctr_digits=0;
$ctr_specialcar=0;
# conver the string to array
@array_pass = split('',$str_pass);
foreach $pass_char (@array_pass)
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
        elsif($pass_char =~ /[$specialchars]/)
        {
                $ctr_specialcar++;
        }
}
# check if we reached minimal length
if($ctr_length<$min_length)
{
        print "Too short, minimum $min_length and got $ctr_length \n";
        exit 1;
}
# check if we reached minimal UPPER case
if($ctr_uppercase<$min_uppercase)
{
        print "Not enough uppercase, minimum $min_uppercase and got $ctr_uppercase \n";
        exit 2;
}
# check if we reached minimal lower case
if($ctr_lowercase<$min_lowercase)
{
        print "Not enough lowercase, minimum $min_lowercase and got $ctr_lowercase \n";
        exit 3;
}
# check if we reached minimal digits
if($ctr_digits<$min_digits)
{
        print "Not enough digits, minimum $min_digits and got $ctr_digits \n";
        exit 4;
}
# check if we reached minimal special characters
if($ctr_specialcar<$min_specialchar)
{
        print "Not enough special characters, minimum $min_specialchar and got $ctr_specialcar \n";
        exit 5;
}
# if you got up to here , meaning you passed it all with success
# we can now return a non error exit
exit 0;
