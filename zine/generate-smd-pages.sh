#!/bin/sh
#
# Generate 84*5 .smd files
# Yes, it's a hack. Shut up.

INPUT="assets/out/iso-codes.json"
OUTPUT="content/variants"

write_header() {
    cat > "${OUTPUT}/${var}/${code}.smd" <<EOF
---
.title = "Вариант ${var}",
.description = "${name}",
.date = .date("1990-01-01T00:00:00"),
.layout = "tables.shtml",
.custom = .{
${valid_data_link}
${invalid_data_link}
    .variant = "${var}",
},
---
EOF
}

if [ ! "${PWD##*/}" = 'zine' ] || [ ! -d "${PWD}/${OUTPUT}" ]
then  >&2 echo 'Incorrect path. Aborting.' & exit 1
fi

for var in $(seq 1 5)
do
    rm -rf "${OUTPUT:?}/${var:?}/"
    mkdir -p "${OUTPUT}/${var}"

    jq -r '.[] | "\(.iso)\t\(.name)"' "$INPUT" | \
        while IFS="$(printf '\t')" read -r code name; do

            valid_data_link=''
            invalid_data_link=''
            if [ -e "assets/out/valid-variant${var}/${name}.json" ]
            then valid_data_link="  .valid_data = \"out/valid-variant${var}/${name}.json\","
            fi
            if [ -e "assets/out/invalid-variant${var}/${name}.json" ]
            then invalid_data_link="  .invalid_data = \"out/invalid-variant${var}/${name}.json\","
            fi

            write_header
        done   
done
