# LaTeX2HTML 2019.2 (Released June 5, 2019)
# Associate internals original text with physical files.


$key = q/fig:example/;
$ref_files{$key} = "$dir".q|user_guide.html|; 
$noresave{$key} = "$nosave";

$key = q/fig:insert-template/;
$ref_files{$key} = "$dir".q|user_guide.html|; 
$noresave{$key} = "$nosave";

1;

