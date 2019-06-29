print "|--------------------------------------------|"
print "|         Starting Character Demo            |"
print "|--------------------------------------------|"

print 'media path = ' + scene.getMediaPath()
# Add asset paths
scene.addAssetPath('mesh', 'mesh')
scene.addAssetPath('motion', 'ChrRachel')
scene.addAssetPath("script", "behaviorsets")
scene.addAssetPath('script', 'scripts')
scene.loadAssetsFromPath("mesh/ChrRachel")
scene.addAssetPath("audio", "C:/data/cache/audio")
scene.loadAssets()


# Set scene parameters and camera
print 'Configuring scene parameters and camera'
scene.setScale(1.0)  #The scale of the scene in meters. By default, the scene scale is set to centimeters (i.e. 0.01)
scene.setBoolAttribute('internalAudio', True) #set to false if using a game engine e.g. unity
scene.setBoolAttribute('delaySpeechIfNeeded', True)
scene.run('default-viewer.py')
'''
camera = getCamera()
camera.setEye(0, 1.71, 1.86)
camera.setCenter(0, 1.5, 0.01) # was set at 1
camera.setUpVector(SrVec(0, 1, 0))
camera.setScale(1)
camera.setFov(0.6)  # was 1.0472
camera.setFarPlane(100)
camera.setNearPlane(0.1)
camera.setAspectRatio(0.966897)
cameraPos = SrVec(0, 1.6, 10)
scene.getPawn('camera').setPosition(cameraPos)
'''
camera = getCamera()
camera.setEye(0.04, 1.61, 1.47)
camera.setCenter(0.03, 1.42, 0.31)
camera.setUpVector(SrVec(0, 1, 0))
camera.setScale(1)
camera.setFov(0.6)
camera.setFarPlane(100)
camera.setNearPlane(0.01)
camera.setAspectRatio(0.879121)
cameraPos = SrVec(0, 1.6, 10)
scene.getPawn('camera').setPosition(cameraPos)
scene.setBoolAttribute('useNewBMLParsing', True)
scene.setBoolAttribute('useFastSpeechParsing', True)

# Long-Shot Camera
obj = scene.getCamera("cameraLongShot")
if obj == None:
    obj = scene.createCamera("cameraLongShot")
obj.setEye(0.04, 1.61, 2.96)
obj.setCenter(0.04, 0.96, 0.03)
obj.setUpVector(SrVec(0, 1, 0))
obj.setScale(1)
obj.setFov(0.6)
obj.setFarPlane(100)
obj.setNearPlane(0.01)
obj.setAspectRatio(0.966897)

# Medium-Shot Camera
obj = scene.getCamera("cameraMediumShot")
if obj == None:
    obj = scene.createCamera("cameraMediumShot")
obj.setEye(0.04, 1.61, 2.34)
obj.setCenter(0.02, 1.46, 1.08)
obj.setUpVector(SrVec(0, 1, 0))
obj.setScale(1)
obj.setFov(0.6)
obj.setFarPlane(100)
obj.setNearPlane(0.01)
obj.setAspectRatio(0.879121)

# Bust Shot
obj = scene.getCamera("cameraBustShot")
if obj == None:
    obj = scene.createCamera("cameraBustShot")
obj.setEye(0.04, 1.61, 1.47)
obj.setCenter(0.03, 1.42, 0.31)
obj.setUpVector(SrVec(0, 1, 0))
obj.setScale(1)
obj.setFov(0.6)
obj.setFarPlane(100)
obj.setNearPlane(0.01)
obj.setAspectRatio(0.879121)


# Close-up camera
obj = scene.getCamera("cameraCloseUp")
if obj == None:
    obj = scene.createCamera("cameraCloseUp")
obj.setEye(0.04, 1.61, 0.48)
obj.setCenter(0.06, 1.58, 0)
obj.setUpVector(SrVec(0, 1, 0))
obj.setScale(1)
obj.setFov(0.6)
obj.setFarPlane(100)
obj.setNearPlane(0.01)
obj.setAspectRatio(0.966897)

# Extreme Close-Up
obj = scene.getCamera("cameraExtremeCloseUp")
if obj == None:
    obj = scene.createCamera("cameraExtremeCloseUp")
obj.setEye(0.05, 1.62, 0.34)
obj.setCenter(0.06, 1.61, 0)
obj.setUpVector(SrVec(0, 1, 0))
obj.setScale(1)
obj.setFov(0.6)
obj.setFarPlane(100)
obj.setNearPlane(0.01)
obj.setAspectRatio(0.879121)

# HeadShoulders Camera
obj = scene.getCamera("cameraHeadShoulders")
if obj == None:
    obj = scene.createCamera("cameraHeadShoulders")
obj.setEye(0.04, 1.61, 0.66)
obj.setCenter(0.05, 1.58, 0)
obj.setUpVector(SrVec(0, 1, 0))
obj.setScale(1)
obj.setFov(0.6)
obj.setFarPlane(100)
obj.setNearPlane(0.01)
obj.setAspectRatio(0.879121)


# ---- light: light0
obj = scene.getPawn("light0")
if obj == None:
	obj = scene.createPawn("light0")
obj.setPosition(SrVec(0, 0, 0))
obj.setOrientation(SrQuat(0.5432, -0.802058, -0.248032, 0.0108262))
if obj.getAttribute("blendTexturesWithLighting") != None :
	obj.setBoolAttribute("blendTexturesWithLighting",True)
else:
	attr = obj.createBoolAttribute("blendTexturesWithLighting", True, True, "Display", 405, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("collisionShape") != None :
	obj.setStringAttribute("collisionShape","null")
else:
	attr = obj.createStringAttribute("collisionShape",  "null", True, "Physics", 350, False, False, False, "Initializes the pawn as a physics object.")
	attr.setDefaultValue("null")
	attr.setValue("null")
	validValues = StringVec()
	validValues.append("null")
	validValues.append("sphere")
	validValues.append("box")
	validValues.append("capsule")
	attr.setValidValues(validValues)
if obj.getAttribute("collisionShapeScale") != None :
	obj.setVec3Attribute("collisionShapeScale",1, 1, 1)
else:
	attr = obj.createVec3Attribute("collisionShapeScale",  1, 1, 1, True, "Physics", 360, False, False, False, "Scaling of physics-based shape.")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 1)
	vec.setData(2, 1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 1, 1)
	attr.setValue(vec1)
if obj.getAttribute("color") != None :
	obj.setVec3Attribute("color",1, 0, 0)
else:
	attr = obj.createVec3Attribute("color",  1, 0, 0, True, "Display", 6, False, False, False, "Object color.")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("enablePhysics") != None :
	obj.setBoolAttribute("enablePhysics",False)
else:
	attr = obj.createBoolAttribute("enablePhysics", False, True, "Physics", 310, False, False, False, "Enables or disables physics for this pawn.")
	attr.setDefaultValue(False)
	attr.setValue(False)
if obj.getAttribute("enabled") != None :
	obj.setBoolAttribute("enabled",True)
else:
	attr = obj.createBoolAttribute("enabled", True, True, "LightParameters", 200, False, False, False, "Is the light enabled?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightAmbientColor") != None :
	obj.setVec3Attribute("lightAmbientColor",0, 0, 0)
else:
	attr = obj.createVec3Attribute("lightAmbientColor",  0, 0, 0, True, "LightParameters", 220, False, False, False, " Ambient light color")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("lightCastShadow") != None :
	obj.setBoolAttribute("lightCastShadow",True)
else:
	attr = obj.createBoolAttribute("lightCastShadow", True, True, "LightParameters", 300, False, False, False, "Does the light cast shadow?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightConstantAttenuation") != None :
	obj.setDoubleAttribute("lightConstantAttenuation",1)
else:
	attr = obj.createDoubleAttribute("lightConstantAttenuation", 1, True, "LightParameters", 270, False, False, False, "Constant attenuation")
	attr.setDefaultValue(1)
	attr.setValue(1)
if obj.getAttribute("lightDiffuseColor") != None :
	obj.setVec3Attribute("lightDiffuseColor",0.9, 0.9, 0.9)
else:
	attr = obj.createVec3Attribute("lightDiffuseColor",  0.9, 0.9, 0.9, True, "LightParameters", 210, False, False, False, " Diffuse light color")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 0.95)
	vec.setData(2, 0.8)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0.9, 0.9, 0.9)
	attr.setValue(vec1)
if obj.getAttribute("lightIsDirectional") != None :
	obj.setBoolAttribute("lightIsDirectional",True)
else:
	attr = obj.createBoolAttribute("lightIsDirectional", True, True, "LightParameters", 205, False, False, False, "Is the light directional?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightLinearAttenuation") != None :
	obj.setDoubleAttribute("lightLinearAttenuation",1)
else:
	attr = obj.createDoubleAttribute("lightLinearAttenuation", 1, True, "LightParameters", 280, False, False, False, " Linear attenuation.")
	attr.setDefaultValue(1)
	attr.setValue(1)
if obj.getAttribute("lightQuadraticAttenuation") != None :
	obj.setDoubleAttribute("lightQuadraticAttenuation",0)
else:
	attr = obj.createDoubleAttribute("lightQuadraticAttenuation", 0, True, "LightParameters", 290, False, False, False, "Quadratic attenuation")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("lightShadowMapSize") != None :
	obj.setIntAttribute("lightShadowMapSize",1024)
else:
	attr = obj.createIntAttribute("lightShadowMapSize", 1024, True, "LightParameters", 310, False, False, False, "Size of the shadow map")
	attr.setDefaultValue(1024)
	attr.setValue(1024)
if obj.getAttribute("lightSpecularColor") != None :
	obj.setVec3Attribute("lightSpecularColor",0, 0, 0)
else:
	attr = obj.createVec3Attribute("lightSpecularColor",  0, 0, 0, True, "LightParameters", 230, False, False, False, "Specular light color")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("lightSpotCutoff") != None :
	obj.setDoubleAttribute("lightSpotCutoff",180)
else:
	attr = obj.createDoubleAttribute("lightSpotCutoff", 180, True, "LightParameters", 260, False, False, False, "Spotlight cutoff angle")
	attr.setDefaultValue(180)
	attr.setValue(180)
if obj.getAttribute("lightSpotDirection") != None :
	obj.setVec3Attribute("lightSpotDirection",0, 0, -1)
else:
	attr = obj.createVec3Attribute("lightSpotDirection",  0, 0, -1, True, "LightParameters", 250, False, False, False, "Spotlight direction")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, -1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, -1)
	attr.setValue(vec1)
if obj.getAttribute("lightSpotExponent") != None :
	obj.setDoubleAttribute("lightSpotExponent",0)
else:
	attr = obj.createDoubleAttribute("lightSpotExponent", 0, True, "LightParameters", 240, False, False, False, " Spotlight exponent.")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("mesh") != None :
	obj.setStringAttribute("mesh","")
else:
	attr = obj.createStringAttribute("mesh",  "", True, "Display", 400, False, False, False, "Geometry/mesh")
	attr.setDefaultValue("")
	attr.setValue("")
	validValues = StringVec()
	attr.setValidValues(validValues)
if obj.getAttribute("meshPivot") != None :
	obj.setVec3Attribute("meshPivot",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshPivot",  0, 0, 0, True, "Display", 440, False, False, False, "Mesh pivot offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("meshRotation") != None :
	obj.setVec3Attribute("meshRotation",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshRotation",  0, 0, 0, True, "Display", 430, False, False, False, "Mesh rotation offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("meshScale") != None :
	obj.setVec3Attribute("meshScale",1, 1, 1)
else:
	attr = obj.createVec3Attribute("meshScale",  1, 1, 1, True, "Display", 410, False, False, False, "Scale of geometry/mesh")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 1)
	vec.setData(2, 1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 1, 1)
	attr.setValue(vec1)
if obj.getAttribute("meshTranslation") != None :
	obj.setVec3Attribute("meshTranslation",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshTranslation",  0, 0, 0, True, "Display", 420, False, False, False, "Mesh translation offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",0)
else:
	attr = obj.createDoubleAttribute("posX", 0, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",0)
else:
	attr = obj.createDoubleAttribute("posY", 0, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",0)
else:
	attr = obj.createDoubleAttribute("posZ", 0, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("rotX") != None :
	obj.setDoubleAttribute("rotX",-59.9954)
else:
	attr = obj.createDoubleAttribute("rotX", -59.9954, True, "transform", 40, False, False, False, "X rotation")
	attr.setDefaultValue(0)
	attr.setValue(-59.9954)
if obj.getAttribute("rotY") != None :
	obj.setDoubleAttribute("rotY",-145)
else:
	attr = obj.createDoubleAttribute("rotY", -145, True, "transform", 50, False, False, False, "Y rotation")
	attr.setDefaultValue(0)
	attr.setValue(-145)
if obj.getAttribute("rotZ") != None :
	obj.setDoubleAttribute("rotZ",125)
else:
	attr = obj.createDoubleAttribute("rotZ", 125, True, "transform", 60, False, False, False, "Z rotation")
	attr.setDefaultValue(0)
	attr.setValue(125)
if obj.getAttribute("showCollisionShape") != None :
	obj.setBoolAttribute("showCollisionShape",True)
else:
	attr = obj.createBoolAttribute("showCollisionShape", True, True, "Physics", 370, False, False, False, "Whether the collision shape is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("showStaticMesh") != None :
	obj.setBoolAttribute("showStaticMesh",True)
else:
	attr = obj.createBoolAttribute("showStaticMesh", True, True, "Display", 405, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("visible") != None :
	obj.setBoolAttribute("visible",False)
else:
	attr = obj.createBoolAttribute("visible", False, True, "Display", 5, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(False)

# ---- light: light1
obj = scene.getPawn("light1")
if obj == None:
	obj = scene.createPawn("light1")
obj.setPosition(SrVec(0, 0, 0))
obj.setOrientation(SrQuat(-0.232125, -0.749725, -0.262516, 0.561352))
if obj.getAttribute("blendTexturesWithLighting") != None :
	obj.setBoolAttribute("blendTexturesWithLighting",True)
else:
	attr = obj.createBoolAttribute("blendTexturesWithLighting", True, True, "Display", 405, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("collisionShape") != None :
	obj.setStringAttribute("collisionShape","null")
else:
	attr = obj.createStringAttribute("collisionShape",  "null", True, "Physics", 350, False, False, False, "Initializes the pawn as a physics object.")
	attr.setDefaultValue("null")
	attr.setValue("null")
	validValues = StringVec()
	validValues.append("null")
	validValues.append("sphere")
	validValues.append("box")
	validValues.append("capsule")
	attr.setValidValues(validValues)
if obj.getAttribute("collisionShapeScale") != None :
	obj.setVec3Attribute("collisionShapeScale",1, 1, 1)
else:
	attr = obj.createVec3Attribute("collisionShapeScale",  1, 1, 1, True, "Physics", 360, False, False, False, "Scaling of physics-based shape.")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 1)
	vec.setData(2, 1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 1, 1)
	attr.setValue(vec1)
if obj.getAttribute("color") != None :
	obj.setVec3Attribute("color",1, 0, 0)
else:
	attr = obj.createVec3Attribute("color",  1, 0, 0, True, "Display", 6, False, False, False, "Object color.")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("enablePhysics") != None :
	obj.setBoolAttribute("enablePhysics",False)
else:
	attr = obj.createBoolAttribute("enablePhysics", False, True, "Physics", 310, False, False, False, "Enables or disables physics for this pawn.")
	attr.setDefaultValue(False)
	attr.setValue(False)
if obj.getAttribute("enabled") != None :
	obj.setBoolAttribute("enabled",True)
else:
	attr = obj.createBoolAttribute("enabled", True, True, "LightParameters", 200, False, False, False, "Is the light enabled?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightAmbientColor") != None :
	obj.setVec3Attribute("lightAmbientColor",0, 0, 0)
else:
	attr = obj.createVec3Attribute("lightAmbientColor",  0, 0, 0, True, "LightParameters", 220, False, False, False, " Ambient light color")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("lightCastShadow") != None :
	obj.setBoolAttribute("lightCastShadow",True)
else:
	attr = obj.createBoolAttribute("lightCastShadow", True, True, "LightParameters", 300, False, False, False, "Does the light cast shadow?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightConstantAttenuation") != None :
	obj.setDoubleAttribute("lightConstantAttenuation",1)
else:
	attr = obj.createDoubleAttribute("lightConstantAttenuation", 1, True, "LightParameters", 270, False, False, False, "Constant attenuation")
	attr.setDefaultValue(1)
	attr.setValue(1)
if obj.getAttribute("lightDiffuseColor") != None :
	obj.setVec3Attribute("lightDiffuseColor",0.9, 0.9, 0.9)
else:
	attr = obj.createVec3Attribute("lightDiffuseColor",  0.9, 0.9, 0.9, True, "LightParameters", 210, False, False, False, " Diffuse light color")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 0.95)
	vec.setData(2, 0.8)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0.9, 0.9, 0.9)
	attr.setValue(vec1)
if obj.getAttribute("lightIsDirectional") != None :
	obj.setBoolAttribute("lightIsDirectional",True)
else:
	attr = obj.createBoolAttribute("lightIsDirectional", True, True, "LightParameters", 205, False, False, False, "Is the light directional?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightLinearAttenuation") != None :
	obj.setDoubleAttribute("lightLinearAttenuation",1)
else:
	attr = obj.createDoubleAttribute("lightLinearAttenuation", 1, True, "LightParameters", 280, False, False, False, " Linear attenuation.")
	attr.setDefaultValue(1)
	attr.setValue(1)
if obj.getAttribute("lightQuadraticAttenuation") != None :
	obj.setDoubleAttribute("lightQuadraticAttenuation",0)
else:
	attr = obj.createDoubleAttribute("lightQuadraticAttenuation", 0, True, "LightParameters", 290, False, False, False, "Quadratic attenuation")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("lightShadowMapSize") != None :
	obj.setIntAttribute("lightShadowMapSize",1024)
else:
	attr = obj.createIntAttribute("lightShadowMapSize", 1024, True, "LightParameters", 310, False, False, False, "Size of the shadow map")
	attr.setDefaultValue(1024)
	attr.setValue(1024)
if obj.getAttribute("lightSpecularColor") != None :
	obj.setVec3Attribute("lightSpecularColor",0, 0, 0)
else:
	attr = obj.createVec3Attribute("lightSpecularColor",  0, 0, 0, True, "LightParameters", 230, False, False, False, "Specular light color")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("lightSpotCutoff") != None :
	obj.setDoubleAttribute("lightSpotCutoff",180)
else:
	attr = obj.createDoubleAttribute("lightSpotCutoff", 180, True, "LightParameters", 260, False, False, False, "Spotlight cutoff angle")
	attr.setDefaultValue(180)
	attr.setValue(180)
if obj.getAttribute("lightSpotDirection") != None :
	obj.setVec3Attribute("lightSpotDirection",0, 0, -1)
else:
	attr = obj.createVec3Attribute("lightSpotDirection",  0, 0, -1, True, "LightParameters", 250, False, False, False, "Spotlight direction")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, -1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, -1)
	attr.setValue(vec1)
if obj.getAttribute("lightSpotExponent") != None :
	obj.setDoubleAttribute("lightSpotExponent",0)
else:
	attr = obj.createDoubleAttribute("lightSpotExponent", 0, True, "LightParameters", 240, False, False, False, " Spotlight exponent.")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("mesh") != None :
	obj.setStringAttribute("mesh","")
else:
	attr = obj.createStringAttribute("mesh",  "", True, "Display", 400, False, False, False, "Geometry/mesh")
	attr.setDefaultValue("")
	attr.setValue("")
	validValues = StringVec()
	attr.setValidValues(validValues)
if obj.getAttribute("meshPivot") != None :
	obj.setVec3Attribute("meshPivot",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshPivot",  0, 0, 0, True, "Display", 440, False, False, False, "Mesh pivot offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("meshRotation") != None :
	obj.setVec3Attribute("meshRotation",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshRotation",  0, 0, 0, True, "Display", 430, False, False, False, "Mesh rotation offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("meshScale") != None :
	obj.setVec3Attribute("meshScale",1, 1, 1)
else:
	attr = obj.createVec3Attribute("meshScale",  1, 1, 1, True, "Display", 410, False, False, False, "Scale of geometry/mesh")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 1)
	vec.setData(2, 1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 1, 1)
	attr.setValue(vec1)
if obj.getAttribute("meshTranslation") != None :
	obj.setVec3Attribute("meshTranslation",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshTranslation",  0, 0, 0, True, "Display", 420, False, False, False, "Mesh translation offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",0)
else:
	attr = obj.createDoubleAttribute("posX", 0, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",0)
else:
	attr = obj.createDoubleAttribute("posY", 0, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",0)
else:
	attr = obj.createDoubleAttribute("posZ", 0, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("rotX") != None :
	obj.setDoubleAttribute("rotX",40)
else:
	attr = obj.createDoubleAttribute("rotX", 40, True, "transform", 40, False, False, False, "X rotation")
	attr.setDefaultValue(0)
	attr.setValue(40)
if obj.getAttribute("rotY") != None :
	obj.setDoubleAttribute("rotY",-110)
else:
	attr = obj.createDoubleAttribute("rotY", -110, True, "transform", 50, False, False, False, "Y rotation")
	attr.setDefaultValue(0)
	attr.setValue(-110)
if obj.getAttribute("rotZ") != None :
	obj.setDoubleAttribute("rotZ",170)
else:
	attr = obj.createDoubleAttribute("rotZ", 170, True, "transform", 60, False, False, False, "Z rotation")
	attr.setDefaultValue(0)
	attr.setValue(170)
if obj.getAttribute("showCollisionShape") != None :
	obj.setBoolAttribute("showCollisionShape",True)
else:
	attr = obj.createBoolAttribute("showCollisionShape", True, True, "Physics", 370, False, False, False, "Whether the collision shape is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("showStaticMesh") != None :
	obj.setBoolAttribute("showStaticMesh",True)
else:
	attr = obj.createBoolAttribute("showStaticMesh", True, True, "Display", 405, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("visible") != None :
	obj.setBoolAttribute("visible",False)
else:
	attr = obj.createBoolAttribute("visible", False, True, "Display", 5, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(False)

# ---- light: light2
obj = scene.getPawn("light2")
if obj == None:
	obj = scene.createPawn("light2")
obj.setPosition(SrVec(6.85, 0, 0))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("blendTexturesWithLighting") != None :
	obj.setBoolAttribute("blendTexturesWithLighting",True)
else:
	attr = obj.createBoolAttribute("blendTexturesWithLighting", True, True, "Display", 405, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("collisionShape") != None :
	obj.setStringAttribute("collisionShape","null")
else:
	attr = obj.createStringAttribute("collisionShape",  "null", True, "Physics", 350, False, False, False, "Initializes the pawn as a physics object.")
	attr.setDefaultValue("null")
	attr.setValue("null")
	validValues = StringVec()
	validValues.append("null")
	validValues.append("sphere")
	validValues.append("box")
	validValues.append("capsule")
	attr.setValidValues(validValues)
if obj.getAttribute("collisionShapeScale") != None :
	obj.setVec3Attribute("collisionShapeScale",1, 1, 1)
else:
	attr = obj.createVec3Attribute("collisionShapeScale",  1, 1, 1, True, "Physics", 360, False, False, False, "Scaling of physics-based shape.")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 1)
	vec.setData(2, 1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 1, 1)
	attr.setValue(vec1)
if obj.getAttribute("color") != None :
	obj.setVec3Attribute("color",1, 0, 0)
else:
	attr = obj.createVec3Attribute("color",  1, 0, 0, True, "Display", 6, False, False, False, "Object color.")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("enablePhysics") != None :
	obj.setBoolAttribute("enablePhysics",False)
else:
	attr = obj.createBoolAttribute("enablePhysics", False, True, "Physics", 310, False, False, False, "Enables or disables physics for this pawn.")
	attr.setDefaultValue(False)
	attr.setValue(False)
if obj.getAttribute("enabled") != None :
	obj.setBoolAttribute("enabled",True)
else:
	attr = obj.createBoolAttribute("enabled", True, True, "LightParameters", 200, False, False, False, "Is the light enabled?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightAmbientColor") != None :
	obj.setVec3Attribute("lightAmbientColor",0, 0, 0)
else:
	attr = obj.createVec3Attribute("lightAmbientColor",  0, 0, 0, True, "LightParameters", 220, False, False, False, " Ambient light color")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("lightCastShadow") != None :
	obj.setBoolAttribute("lightCastShadow",True)
else:
	attr = obj.createBoolAttribute("lightCastShadow", True, True, "LightParameters", 300, False, False, False, "Does the light cast shadow?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightConstantAttenuation") != None :
	obj.setDoubleAttribute("lightConstantAttenuation",1)
else:
	attr = obj.createDoubleAttribute("lightConstantAttenuation", 1, True, "LightParameters", 270, False, False, False, "Constant attenuation")
	attr.setDefaultValue(1)
	attr.setValue(1)
if obj.getAttribute("lightDiffuseColor") != None :
	obj.setVec3Attribute("lightDiffuseColor",1, 0.95, 0.8)
else:
	attr = obj.createVec3Attribute("lightDiffuseColor",  1, 0.95, 0.8, True, "LightParameters", 210, False, False, False, " Diffuse light color")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 0.95)
	vec.setData(2, 0.8)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 0.95, 0.8)
	attr.setValue(vec1)
if obj.getAttribute("lightIsDirectional") != None :
	obj.setBoolAttribute("lightIsDirectional",False)
else:
	attr = obj.createBoolAttribute("lightIsDirectional", False, True, "LightParameters", 205, False, False, False, "Is the light directional?")
	attr.setDefaultValue(True)
	attr.setValue(False)
if obj.getAttribute("lightLinearAttenuation") != None :
	obj.setDoubleAttribute("lightLinearAttenuation",1)
else:
	attr = obj.createDoubleAttribute("lightLinearAttenuation", 1, True, "LightParameters", 280, False, False, False, " Linear attenuation.")
	attr.setDefaultValue(1)
	attr.setValue(1)
if obj.getAttribute("lightQuadraticAttenuation") != None :
	obj.setDoubleAttribute("lightQuadraticAttenuation",0)
else:
	attr = obj.createDoubleAttribute("lightQuadraticAttenuation", 0, True, "LightParameters", 290, False, False, False, "Quadratic attenuation")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("lightShadowMapSize") != None :
	obj.setIntAttribute("lightShadowMapSize",1024)
else:
	attr = obj.createIntAttribute("lightShadowMapSize", 1024, True, "LightParameters", 310, False, False, False, "Size of the shadow map")
	attr.setDefaultValue(1024)
	attr.setValue(1024)
if obj.getAttribute("lightSpecularColor") != None :
	obj.setVec3Attribute("lightSpecularColor",0, 0, 0)
else:
	attr = obj.createVec3Attribute("lightSpecularColor",  0, 0, 0, True, "LightParameters", 230, False, False, False, "Specular light color")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("lightSpotCutoff") != None :
	obj.setDoubleAttribute("lightSpotCutoff",180)
else:
	attr = obj.createDoubleAttribute("lightSpotCutoff", 180, True, "LightParameters", 260, False, False, False, "Spotlight cutoff angle")
	attr.setDefaultValue(180)
	attr.setValue(180)
if obj.getAttribute("lightSpotDirection") != None :
	obj.setVec3Attribute("lightSpotDirection",0, 0, -1)
else:
	attr = obj.createVec3Attribute("lightSpotDirection",  0, 0, -1, True, "LightParameters", 250, False, False, False, "Spotlight direction")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, -1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, -1)
	attr.setValue(vec1)
if obj.getAttribute("lightSpotExponent") != None :
	obj.setDoubleAttribute("lightSpotExponent",0)
else:
	attr = obj.createDoubleAttribute("lightSpotExponent", 0, True, "LightParameters", 240, False, False, False, " Spotlight exponent.")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("mesh") != None :
	obj.setStringAttribute("mesh","")
else:
	attr = obj.createStringAttribute("mesh",  "", True, "Display", 400, False, False, False, "Geometry/mesh")
	attr.setDefaultValue("")
	attr.setValue("")
	validValues = StringVec()
	attr.setValidValues(validValues)
if obj.getAttribute("meshPivot") != None :
	obj.setVec3Attribute("meshPivot",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshPivot",  0, 0, 0, True, "Display", 440, False, False, False, "Mesh pivot offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("meshRotation") != None :
	obj.setVec3Attribute("meshRotation",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshRotation",  0, 0, 0, True, "Display", 430, False, False, False, "Mesh rotation offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("meshScale") != None :
	obj.setVec3Attribute("meshScale",1, 1, 1)
else:
	attr = obj.createVec3Attribute("meshScale",  1, 1, 1, True, "Display", 410, False, False, False, "Scale of geometry/mesh")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 1)
	vec.setData(2, 1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 1, 1)
	attr.setValue(vec1)
if obj.getAttribute("meshTranslation") != None :
	obj.setVec3Attribute("meshTranslation",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshTranslation",  0, 0, 0, True, "Display", 420, False, False, False, "Mesh translation offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",6.85)
else:
	attr = obj.createDoubleAttribute("posX", 6.85, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(6.85)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",0)
else:
	attr = obj.createDoubleAttribute("posY", 0, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",0)
else:
	attr = obj.createDoubleAttribute("posZ", 0, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("rotX") != None :
	obj.setDoubleAttribute("rotX",-0)
else:
	attr = obj.createDoubleAttribute("rotX", -0, True, "transform", 40, False, False, False, "X rotation")
	attr.setDefaultValue(0)
	attr.setValue(-0)
if obj.getAttribute("rotY") != None :
	obj.setDoubleAttribute("rotY",0)
else:
	attr = obj.createDoubleAttribute("rotY", 0, True, "transform", 50, False, False, False, "Y rotation")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("rotZ") != None :
	obj.setDoubleAttribute("rotZ",0)
else:
	attr = obj.createDoubleAttribute("rotZ", 0, True, "transform", 60, False, False, False, "Z rotation")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("showCollisionShape") != None :
	obj.setBoolAttribute("showCollisionShape",True)
else:
	attr = obj.createBoolAttribute("showCollisionShape", True, True, "Physics", 370, False, False, False, "Whether the collision shape is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("showStaticMesh") != None :
	obj.setBoolAttribute("showStaticMesh",True)
else:
	attr = obj.createBoolAttribute("showStaticMesh", True, True, "Display", 405, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("visible") != None :
	obj.setBoolAttribute("visible",False)
else:
	attr = obj.createBoolAttribute("visible", False, True, "Display", 5, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(False)# ---- pawn: camera
obj = scene.getPawn("camera")
if obj == None:
	obj = scene.createPawn("camera")
obj.setPosition(SrVec(0, 1.6, 10))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",1.6)
else:
	attr = obj.createDoubleAttribute("posY", 1.6, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(1.6)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",10)
else:
	attr = obj.createDoubleAttribute("posZ", 10, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(10)

# ---- light: light3
obj = scene.getPawn("light3")
if obj == None:
	obj = scene.createPawn("light3")
obj.setPosition(SrVec(0, 0, 0))
obj.setOrientation(SrQuat(0.92388, 0.382683, 0, 0))
if obj.getAttribute("blendTexturesWithLighting") != None :
	obj.setBoolAttribute("blendTexturesWithLighting",True)
else:
	attr = obj.createBoolAttribute("blendTexturesWithLighting", True, True, "Display", 405, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("collisionShape") != None :
	obj.setStringAttribute("collisionShape","null")
else:
	attr = obj.createStringAttribute("collisionShape",  "null", True, "Physics", 350, False, False, False, "Initializes the pawn as a physics object.")
	attr.setDefaultValue("null")
	attr.setValue("null")
	validValues = StringVec()
	validValues.append("null")
	validValues.append("sphere")
	validValues.append("box")
	validValues.append("capsule")
	attr.setValidValues(validValues)
if obj.getAttribute("collisionShapeScale") != None :
	obj.setVec3Attribute("collisionShapeScale",1, 1, 1)
else:
	attr = obj.createVec3Attribute("collisionShapeScale",  1, 1, 1, True, "Physics", 360, False, False, False, "Scaling of physics-based shape.")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 1)
	vec.setData(2, 1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 1, 1)
	attr.setValue(vec1)
if obj.getAttribute("color") != None :
	obj.setVec3Attribute("color",1, 0, 0)
else:
	attr = obj.createVec3Attribute("color",  1, 0, 0, True, "Display", 6, False, False, False, "Object color.")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("enablePhysics") != None :
	obj.setBoolAttribute("enablePhysics",False)
else:
	attr = obj.createBoolAttribute("enablePhysics", False, True, "Physics", 310, False, False, False, "Enables or disables physics for this pawn.")
	attr.setDefaultValue(False)
	attr.setValue(False)
if obj.getAttribute("enabled") != None :
	obj.setBoolAttribute("enabled",True)
else:
	attr = obj.createBoolAttribute("enabled", True, True, "LightParameters", 200, False, False, False, "Is the light enabled?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightAmbientColor") != None :
	obj.setVec3Attribute("lightAmbientColor",0, 0, 0)
else:
	attr = obj.createVec3Attribute("lightAmbientColor",  0, 0, 0, True, "LightParameters", 220, False, False, False, " Ambient light color")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("lightCastShadow") != None :
	obj.setBoolAttribute("lightCastShadow",True)
else:
	attr = obj.createBoolAttribute("lightCastShadow", True, True, "LightParameters", 300, False, False, False, "Does the light cast shadow?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightConstantAttenuation") != None :
	obj.setDoubleAttribute("lightConstantAttenuation",1)
else:
	attr = obj.createDoubleAttribute("lightConstantAttenuation", 1, True, "LightParameters", 270, False, False, False, "Constant attenuation")
	attr.setDefaultValue(1)
	attr.setValue(1)
if obj.getAttribute("lightDiffuseColor") != None :
	obj.setVec3Attribute("lightDiffuseColor",1, 0.95, 0.8)
else:
	attr = obj.createVec3Attribute("lightDiffuseColor",  1, 0.95, 0.8, True, "LightParameters", 210, False, False, False, " Diffuse light color")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 0.95)
	vec.setData(2, 0.8)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 0.95, 0.8)
	attr.setValue(vec1)
if obj.getAttribute("lightIsDirectional") != None :
	obj.setBoolAttribute("lightIsDirectional",True)
else:
	attr = obj.createBoolAttribute("lightIsDirectional", True, True, "LightParameters", 205, False, False, False, "Is the light directional?")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("lightLinearAttenuation") != None :
	obj.setDoubleAttribute("lightLinearAttenuation",1)
else:
	attr = obj.createDoubleAttribute("lightLinearAttenuation", 1, True, "LightParameters", 280, False, False, False, " Linear attenuation.")
	attr.setDefaultValue(1)
	attr.setValue(1)
if obj.getAttribute("lightQuadraticAttenuation") != None :
	obj.setDoubleAttribute("lightQuadraticAttenuation",0)
else:
	attr = obj.createDoubleAttribute("lightQuadraticAttenuation", 0, True, "LightParameters", 290, False, False, False, "Quadratic attenuation")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("lightShadowMapSize") != None :
	obj.setIntAttribute("lightShadowMapSize",1024)
else:
	attr = obj.createIntAttribute("lightShadowMapSize", 1024, True, "LightParameters", 310, False, False, False, "Size of the shadow map")
	attr.setDefaultValue(1024)
	attr.setValue(1024)
if obj.getAttribute("lightSpecularColor") != None :
	obj.setVec3Attribute("lightSpecularColor",0, 0, 0)
else:
	attr = obj.createVec3Attribute("lightSpecularColor",  0, 0, 0, True, "LightParameters", 230, False, False, False, "Specular light color")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("lightSpotCutoff") != None :
	obj.setDoubleAttribute("lightSpotCutoff",180)
else:
	attr = obj.createDoubleAttribute("lightSpotCutoff", 180, True, "LightParameters", 260, False, False, False, "Spotlight cutoff angle")
	attr.setDefaultValue(180)
	attr.setValue(180)
if obj.getAttribute("lightSpotDirection") != None :
	obj.setVec3Attribute("lightSpotDirection",0, 0, -1)
else:
	attr = obj.createVec3Attribute("lightSpotDirection",  0, 0, -1, True, "LightParameters", 250, False, False, False, "Spotlight direction")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, -1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, -1)
	attr.setValue(vec1)
if obj.getAttribute("lightSpotExponent") != None :
	obj.setDoubleAttribute("lightSpotExponent",0)
else:
	attr = obj.createDoubleAttribute("lightSpotExponent", 0, True, "LightParameters", 240, False, False, False, " Spotlight exponent.")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("mesh") != None :
	obj.setStringAttribute("mesh","")
else:
	attr = obj.createStringAttribute("mesh",  "", True, "Display", 400, False, False, False, "Geometry/mesh")
	attr.setDefaultValue("")
	attr.setValue("")
	validValues = StringVec()
	attr.setValidValues(validValues)
if obj.getAttribute("meshPivot") != None :
	obj.setVec3Attribute("meshPivot",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshPivot",  0, 0, 0, True, "Display", 440, False, False, False, "Mesh pivot offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("meshRotation") != None :
	obj.setVec3Attribute("meshRotation",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshRotation",  0, 0, 0, True, "Display", 430, False, False, False, "Mesh rotation offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("meshScale") != None :
	obj.setVec3Attribute("meshScale",1, 1, 1)
else:
	attr = obj.createVec3Attribute("meshScale",  1, 1, 1, True, "Display", 410, False, False, False, "Scale of geometry/mesh")
	vec = SrVec()
	vec.setData(0, 1)
	vec.setData(1, 1)
	vec.setData(2, 1)
	attr.setDefaultValue(vec)
	vec1 = SrVec(1, 1, 1)
	attr.setValue(vec1)
if obj.getAttribute("meshTranslation") != None :
	obj.setVec3Attribute("meshTranslation",0, 0, 0)
else:
	attr = obj.createVec3Attribute("meshTranslation",  0, 0, 0, True, "Display", 420, False, False, False, "Mesh translation offset")
	vec = SrVec()
	vec.setData(0, 0)
	vec.setData(1, 0)
	vec.setData(2, 0)
	attr.setDefaultValue(vec)
	vec1 = SrVec(0, 0, 0)
	attr.setValue(vec1)
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",0)
else:
	attr = obj.createDoubleAttribute("posX", 0, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",0)
else:
	attr = obj.createDoubleAttribute("posY", 0, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",0)
else:
	attr = obj.createDoubleAttribute("posZ", 0, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("rotX") != None :
	obj.setDoubleAttribute("rotX",45)
else:
	attr = obj.createDoubleAttribute("rotX", 45, True, "transform", 40, False, False, False, "X rotation")
	attr.setDefaultValue(0)
	attr.setValue(45)
if obj.getAttribute("rotY") != None :
	obj.setDoubleAttribute("rotY",0)
else:
	attr = obj.createDoubleAttribute("rotY", 0, True, "transform", 50, False, False, False, "Y rotation")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("rotZ") != None :
	obj.setDoubleAttribute("rotZ",0)
else:
	attr = obj.createDoubleAttribute("rotZ", 0, True, "transform", 60, False, False, False, "Z rotation")
	attr.setDefaultValue(0)
	attr.setValue(0)
if obj.getAttribute("showCollisionShape") != None :
	obj.setBoolAttribute("showCollisionShape",True)
else:
	attr = obj.createBoolAttribute("showCollisionShape", True, True, "Physics", 370, False, False, False, "Whether the collision shape is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("showStaticMesh") != None :
	obj.setBoolAttribute("showStaticMesh",True)
else:
	attr = obj.createBoolAttribute("showStaticMesh", True, True, "Display", 405, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(True)
if obj.getAttribute("visible") != None :
	obj.setBoolAttribute("visible",False)
else:
	attr = obj.createBoolAttribute("visible", False, True, "Display", 5, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(False)
	
# ---- pawn: pawnLeftDown
obj = scene.getPawn("pawnLeftDown")
if obj == None:
	obj = scene.createPawn("pawnLeftDown")
obj.setPosition(SrVec(1, 0.7, 6))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",1)
else:
	attr = obj.createDoubleAttribute("posX", 1, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(1)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",0.7)
else:
	attr = obj.createDoubleAttribute("posY", 0.7, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(0.7)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",6)
else:
	attr = obj.createDoubleAttribute("posZ", 6, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(6)
if obj.getAttribute("visible") != None :
	obj.setBoolAttribute("visible",False)
else:
	attr = obj.createBoolAttribute("visible", False, True, "Display", 5, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(False)

# ---- pawn: pawnRightDown
obj = scene.getPawn("pawnRightDown")
if obj == None:
	obj = scene.createPawn("pawnRightDown")
obj.setPosition(SrVec(-0.7, 0.5, 6))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",-0.7)
else:
	attr = obj.createDoubleAttribute("posX", -0.7, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(-0.7)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",0.5)
else:
	attr = obj.createDoubleAttribute("posY", 0.5, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(0.5)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",6)
else:
	attr = obj.createDoubleAttribute("posZ", 6, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(6)
if obj.getAttribute("visible") != None :
	obj.setBoolAttribute("visible",False)
else:
	attr = obj.createBoolAttribute("visible", False, True, "Display", 5, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(False)

# ---- pawn: pawnDown
obj = scene.getPawn("pawnDown")
if obj == None:
	obj = scene.createPawn("pawnDown")
obj.setPosition(SrVec(0, 1, 6))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",1)
else:
	attr = obj.createDoubleAttribute("posY", 1, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(1)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",6)
else:
	attr = obj.createDoubleAttribute("posZ", 6, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(6)
if obj.getAttribute("visible") != None :
	obj.setBoolAttribute("visible",False)
else:
	attr = obj.createBoolAttribute("visible", False, True, "Display", 5, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(False)

# ---- pawn: pawnFront
obj = scene.getPawn("pawnFront")
if obj == None:
	obj = scene.createPawn("pawnFront")
obj.setPosition(SrVec(0, 1.6, 2))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",1.6)
else:
	attr = obj.createDoubleAttribute("posY", 1.6, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(1.6)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",2)
else:
	attr = obj.createDoubleAttribute("posZ", 2, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(2)
if obj.getAttribute("visible") != None :
	obj.setBoolAttribute("visible",False)
else:
	attr = obj.createBoolAttribute("visible", False, True, "Display", 5, False, False, False, "Whether the object is visible.")
	attr.setDefaultValue(True)
	attr.setValue(False)

# ---- pawn: pawnLeftTilt
obj = scene.getPawn("pawnLeftTilt")
if obj == None:
	obj = scene.createPawn("pawnLeftTilt")
obj.setPosition(SrVec(0, 6, 2))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",6)
else:
	attr = obj.createDoubleAttribute("posY", 6, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(6)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",2)
else:
	attr = obj.createDoubleAttribute("posZ", 2, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(2)

# ---- pawn: pawnLeft1
obj = scene.getPawn("pawnLeft1")
if obj == None:
	obj = scene.createPawn("pawnLeft1")
obj.setPosition(SrVec(1, 25, 11))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",1)
else:
	attr = obj.createDoubleAttribute("posX", 1, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(1)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",25)
else:
	attr = obj.createDoubleAttribute("posY", 25, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(25)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",11)
else:
	attr = obj.createDoubleAttribute("posZ", 11, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(11)

# ---- pawn: pawnLeft2
obj = scene.getPawn("pawnLeft2")
if obj == None:
	obj = scene.createPawn("pawnLeft2")
obj.setPosition(SrVec(1, 4, 5))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",1)
else:
	attr = obj.createDoubleAttribute("posX", 1, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(1)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",4)
else:
	attr = obj.createDoubleAttribute("posY", 4, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(4)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",5)
else:
	attr = obj.createDoubleAttribute("posZ", 5, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(5)

# ---- pawn: pawnLeft3
obj = scene.getPawn("pawnLeft3")
if obj == None:
	obj = scene.createPawn("pawnLeft3")
obj.setPosition(SrVec(0.5, 5, 5))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",0.5)
else:
	attr = obj.createDoubleAttribute("posX", 0.5, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(0.5)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",5)
else:
	attr = obj.createDoubleAttribute("posY", 5, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(5)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",5)
else:
	attr = obj.createDoubleAttribute("posZ", 5, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(5)

# ---- pawn: pawnRightTilt
obj = scene.getPawn("pawnRightTilt")
if obj == None:
	obj = scene.createPawn("pawnRightTilt")
obj.setPosition(SrVec(-0.3, 6, 2))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",-0.3)
else:
	attr = obj.createDoubleAttribute("posX", -0.3, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(-0.3)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",6)
else:
	attr = obj.createDoubleAttribute("posY", 6, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(6)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",2)
else:
	attr = obj.createDoubleAttribute("posZ", 2, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(2)
	
# ---- pawn: pawnRight1
obj = scene.getPawn("pawnRight1")
if obj == None:
	obj = scene.createPawn("pawnRight1")
obj.setPosition(SrVec(-0.3, 2, 6))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",-2)
else:
	attr = obj.createDoubleAttribute("posX", -0.3, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(-0.3)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",2)
else:
	attr = obj.createDoubleAttribute("posY", 2, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(2)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",6)
else:
	attr = obj.createDoubleAttribute("posZ", 6, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(6)

# ---- pawn: pawnRight2
obj = scene.getPawn("pawnRight2")
if obj == None:
	obj = scene.createPawn("pawnRight2")
obj.setPosition(SrVec(-1, 6, 6))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",-1)
else:
	attr = obj.createDoubleAttribute("posX", -1, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(-1)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",6)
else:
	attr = obj.createDoubleAttribute("posY", 6, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(6)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",6)
else:
	attr = obj.createDoubleAttribute("posZ", 6, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(6)

# ---- pawn: pawnRight3
obj = scene.getPawn("pawnRight3")
if obj == None:
	obj = scene.createPawn("pawnRight3")
obj.setPosition(SrVec(-1.5, 9, 5))
obj.setOrientation(SrQuat(1, 0, 0, 0))
if obj.getAttribute("createPhysics") == None :
	attr = obj.createActionAttribute("createPhysics",  True, "Physics", 300, False, False, False, "Initializes the pawn as a physics object.")
if obj.getAttribute("posX") != None :
	obj.setDoubleAttribute("posX",-1.5)
else:
	attr = obj.createDoubleAttribute("posX", -1.5, True, "transform", 10, False, False, False, "X position")
	attr.setDefaultValue(0)
	attr.setValue(-1.5)
if obj.getAttribute("posY") != None :
	obj.setDoubleAttribute("posY",9)
else:
	attr = obj.createDoubleAttribute("posY", 9, True, "transform", 20, False, False, False, "Y position")
	attr.setDefaultValue(0)
	attr.setValue(9)
if obj.getAttribute("posZ") != None :
	obj.setDoubleAttribute("posZ",5)
else:
	attr = obj.createDoubleAttribute("posZ", 5, True, "transform", 30, False, False, False, "Z position")
	attr.setDefaultValue(0)
	attr.setValue(5)

# Set up joint map for Rachel
print 'Setting up joint map and configuring Rachel\'s skeleton'
scene.run('zebra2-map.py')
zebra2Map = scene.getJointMapManager().getJointMap('zebra2')
RachelSkeleton = scene.getSkeleton('ChrRachel.dae')
RachelSkeleton.rescale(.01)
zebra2Map.applySkeleton(RachelSkeleton)
zebra2Map.applyMotionRecurse('ChrRachel')
	
# Establish lip syncing data set
print('Establishing lip syncing data set')
scene.run('init-diphoneDefault.py')


# Set up face definition
print 'Setting up Rachel\'s face definition'
# Rachel's face definition
RachelFace = scene.createFaceDefinition('ChrRachel')
RachelFace.setFaceNeutral('ChrRachel@face_neutral')
RachelFace.setAU(1,  "left",  "ChrRachel@001_inner_brow_raiser_lf")
RachelFace.setAU(1,  "right", "ChrRachel@001_inner_brow_raiser_rt")
RachelFace.setAU(2,  "left",  "ChrRachel@002_outer_brow_raiser_lf")
RachelFace.setAU(2,  "right", "ChrRachel@002_outer_brow_raiser_rt")
RachelFace.setAU(4,  "left",  "ChrRachel@004_brow_lowerer_lf")
RachelFace.setAU(4,  "right", "ChrRachel@004_brow_lowerer_rt")
RachelFace.setAU(5,  "both",  "ChrRachel@005_upper_lid_raiser")
RachelFace.setAU(6,  "both",  "ChrRachel@006_cheek_raiser")
RachelFace.setAU(7,  "both",  "ChrRachel@007_lid_tightener")
RachelFace.setAU(10, "both",  "ChrRachel@010_upper_lip_raiser")
RachelFace.setAU(12, "left",  "ChrRachel@012_lip_corner_puller_lf")
RachelFace.setAU(12, "right", "ChrRachel@012_lip_corner_puller_rt")
RachelFace.setAU(25, "both",  "ChrRachel@025_lips_part")
RachelFace.setAU(26, "both",  "ChrRachel@026_jaw_drop")
RachelFace.setAU(45, "left",  "ChrRachel@045_blink_lf") 
RachelFace.setAU(45, "right", "ChrRachel@045_blink_rt")
RachelFace.setAU(99, "both", "ChrRachel@099_big_smile")
RachelFace.setAU(100, "both", "ChrRachel@100_small_smile")
RachelFace.setAU(101, "both", "ChrRachel@101_upset")
RachelFace.setAU(102, "both", "ChrRachel@102_skeptical")
RachelFace.setAU(103, "both", "ChrRachel@103_concern")
RachelFace.setAU(104, "both", "ChrRachel@104_disgust")

RachelFace.setViseme("open",    "ChrRachel@open")
RachelFace.setViseme("W",       "ChrRachel@W")
RachelFace.setViseme("ShCh",    "ChrRachel@ShCh")
RachelFace.setViseme("PBM",     "ChrRachel@PBM")
RachelFace.setViseme("FV",      "ChrRachel@FV")
RachelFace.setViseme("wide",    "ChrRachel@wide")
RachelFace.setViseme("tBack",   "ChrRachel@tBack")
RachelFace.setViseme("tRoof",   "ChrRachel@tRoof")
RachelFace.setViseme("tTeeth",  "ChrRachel@tTeeth")


print 'Adding character into scene'
# Set up Rachel
Rachel = scene.createCharacter('ChrRachel', '')
RachelSkeleton = scene.createSkeleton('ChrRachel.dae')

Rachel.setSkeleton(RachelSkeleton)
# Set position
RachelPos = SrVec(0, 0, 0)
Rachel.setPosition(RachelPos)
# Set facing direction
RachelFacing = SrVec(0, 0, 0)
Rachel.setHPR(RachelFacing)
# Set face definition
Rachel.setFaceDefinition(RachelFace)
# Set standard controller

Rachel.createStandardControllers()
# Deformable mesh
Rachel.setVec3Attribute('deformableMeshScale', .01, .01, .01)
Rachel.setStringAttribute('deformableMesh', 'ChrRachel.dae')


#brad.setStringAttribute("displayType", "GPUmesh")


# Lip syncing diphone setup
Rachel.setStringAttribute('lipSyncSetName', 'default')
Rachel.setBoolAttribute('usePhoneBigram', True)
Rachel.setBoolAttribute('lipSyncSplineCurve', True)
Rachel.setDoubleAttribute('lipSyncSmoothWindow', .2)
Rachel.setVoice('remote')
#Rachel.setVoiceCode('Microsoft|Zira|Desktop')
Rachel.setVoiceCode('CereVoice|Isabella|-|English|(East|Coast|America)')
Rachel.setStringAttribute('utterancePolicy', 'queue')
Rachel.setBoolAttribute('gestureUseBlends', True)


'''
import platform
if platform.system() == "Windows":
	windowsVer = platform.platform()
	if windowsVer.find("Windows-7") == 0:
		Rachel.setVoiceCode('Microsoft|Anna')
	else:
		if windowsVer.find("Windows-8") == 0 or windowsVer.find("Windows-post2008Server") == 0:
			Rachel.setVoiceCode('Microsoft|Zira|Desktop')
else: # non-Windows platform, use Festival voices
	Rachel.setVoiceCode('voice_kal_diphone')
'''

# Gesture map setup
Rachel.setStringAttribute('gestureMap', 'ChrRachel')
Rachel.setBoolAttribute('bmlRequest.autoGestureTransition', True)
# Turn on GPU deformable geometry
Rachel.setStringAttribute("displayType", "GPUmesh")

# setup locomotion
scene.run('BehaviorSetMaleMocapLocomotion.py')
setupBehaviorSet()
retargetBehaviorSet('ChrRachel')


# setup gestures
scene.run('BehaviorSetGestures.py')
setupBehaviorSet()
retargetBehaviorSet('ChrRachel')

# setup reach 
scene.run('BehaviorSetReaching.py')
setupBehaviorSet()
retargetBehaviorSet('ChrRachel')

# Set up steering
print 'Setting up steering'
steerManager = scene.getSteerManager()
steerManager.setEnable(False)
Rachel.setBoolAttribute('steering.pathFollowingMode', False) # disable path following mode so that obstacles will be respected
Rachel.setBoolAttribute('gestureRequest.enableTransitionToStroke', True)
Rachel.setBoolAttribute('gestureRequest.gestureLog', True)
steerManager.setEnable(True)
'''
# Set up steering
print 'Setting up steering'
steerManager = scene.getSteerManager()
steerManager.setEnable(False)
Rachel.setBoolAttribute('steering.pathFollowingMode', False) # disable path following mode so that obstacles will be respected
steerManager.setEnable(True)
'''

# Start the simulation
print 'Starting the simulation'
sim.start()

'''
Rachel.setStringAttribute('voiceCode', 'CereVoice|Adam|-|English|(East|Coast|America)')
Rachel.setStringAttribute('voice', 'remote')
Rachel.setStringAttribute('utterancePolicy', 'queue')
Rachel.setBoolAttribute('gestureUseBlends', True)
'''
# Lip syncing diphone setup
#brad.setStringAttribute('lipSyncSetName', 'default')
#brad.setBoolAttribute('usePhoneBigram', True)
#for tts speech, enable the next 2 lines -- setVoice to remote and setVoiceCode to one of the available voices
#brad.setStringAttribute('voiceCode', 'CereVoice|Adam|-|English|(East|Coast|America)')
#brad.setStringAttribute('voice', 'remote')
#brad.setStringAttribute('utterancePolicy', 'queue')
#brad.setBoolAttribute('gestureUseBlends', True)


bml.execBML('ChrRachel', '<body posture="ChrBrad@Idle01"/>')
bml.execBML('ChrRachel', '<saccade mode="listen"/>')
#bml.execBML('ChrRachel', '<gaze sbm:handle="brad" target="camera"/>') #uncommented

sim.resume()
