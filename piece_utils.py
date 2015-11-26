# http://stackoverflow.com/q/8421337
def rotateGeometry(geometry):
    rotated = []
    for i, row in enumerate(geometry):
        for j, cell in enumerate(row):
            while j >= len(rotated):
                rotated.append([])
            rotated[j].append(cell)
    return flipGeometry(rotated)

def flipGeometry(geometry):
    return list(reversed(geometry))

# All unique geometries
def allGeometries(geometry):
    geometries = []
    for shouldFlip in [True, False]:
        for numRotations in range(0, 4):
            workingGeometry = geometry
            if shouldFlip:
                workingGeometry = flipGeometry(workingGeometry)
            for i in range(numRotations):
                workingGeometry = rotateGeometry(workingGeometry)
            if not workingGeometry in geometries:
                geometries.append(workingGeometry)
    return geometries

def importGeometries(filename):
    pieces = {}
    with open(filename, 'r') as spec:
        lines = spec.readlines()

        # Remove commented lines
        lines = [l for l in lines if not l.startswith('#')]

        name = None
        geometry = []
        for l in lines:
            l = l.strip()
            if '===' in l:
                if name:
                    pieces[name] = allGeometries(geometry)
                name = None
                geometry = []
                continue
            if not name:
                name = l
                continue
            else:
                # Turn the line into a list of true/false
                ll = list(l)
                boolList = list(map(lambda c: True if c == 'X' else False, ll))
                geometry.append(boolList)

        if name:
            pieces[name] = allGeometries(geometry)

    return pieces
