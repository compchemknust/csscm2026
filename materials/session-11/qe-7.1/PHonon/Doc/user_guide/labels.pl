# LaTeX2HTML 2019.2 (Released June 5, 2019)
# Associate labels original text with physical files.


$key = q/Sec:para/;
$external_labels{$key} = "$URL/" . q|node17.html|; 
$noresave{$key} = "$nosave";

1;


# LaTeX2HTML 2019.2 (Released June 5, 2019)
# labels from external_latex_labels array.


$key = q/Sec:para/;
$external_latex_labels{$key} = q|5|; 
$noresave{$key} = "$nosave";

$key = q/_/;
$external_latex_labels{$key} = q|<|; 
$noresave{$key} = "$nosave";

1;

