#!/bin/bash

# Define repositories to clone (using SSH links)
echo "======================Cloning the repositories========================="
echo ""
REPOS=(
    "git@github.com:ej2xu/cs108.git"
    "git@github.com:abkds/cs106b-stanford.git"
    "git@github.com:lagorg22/bio.git"
    git@github.com:lagorg22/e-commerce.git
    "git@github.com:SoyDiego/projects-React.git"
)

# Clone each repository
for repo in "${REPOS[@]}"; do
    git clone "$repo"
    echo ""
done
echo ""
echo "======================Cloning Done Successfully========================="

# Run Python scripts
echo "======================Gathering Codefiles========================="
echo ""
python3 extract_codefiles.py
echo ""
echo "======================Codefiles Gathered successfully========================="

echo "======================Cleaning Codefiles========================="
echo ""
python3 process_codefiles.py
echo ""
echo "======================Codefiles Cleaned========================="

echo "======================Removing Unnecessary Directories========================="
echo ""
rm -rf rm -rf cs108/ cs106b-stanford/ bio/ copart_myauto/ free-python-games/ projects-React/ e-commerce/
echo "======================Unnecessary Directories removed========================="
