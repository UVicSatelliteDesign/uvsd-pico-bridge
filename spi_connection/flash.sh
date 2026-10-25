PROJECT_UF2=spi_connection.uf2 

DESTINATION=$1

if [[ -n "$DESTINATION" ]] then
    cp -r ./build/$PROJECT_UF2 $DESTINATION
else 
    echo "Must Provide a desitnation file (must be route to PICO) ex: '/dev/tty*'"
fi