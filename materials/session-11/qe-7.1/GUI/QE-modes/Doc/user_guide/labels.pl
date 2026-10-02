# LaTeX2HTML 2019.2 (Released June 5, 2019)
# Associate labels original text with physical files.


$key = q/fig:example/;
$external_labels{$key} = "$URL/" . q|user_guide.html|; 
$noresave{$key} = "$nosave";

$key = q/fig:insert-template/;
$external_labels{$key} = "$URL/" . q|user_guide.html|; 
$noresave{$key} = "$nosave";

1;


# LaTeX2HTML 2019.2 (Released June 5, 2019)
# labels from external_latex_labels array.


1;

