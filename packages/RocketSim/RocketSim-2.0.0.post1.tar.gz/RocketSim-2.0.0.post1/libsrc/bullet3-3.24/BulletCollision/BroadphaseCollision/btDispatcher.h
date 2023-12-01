/*
Bullet Continuous Collision Detection and Physics Library
Copyright (c) 2003-2006 Erwin Coumans  https://bulletphysics.org

This software is provided 'as-is', without any express or implied warranty.
In no event will the authors be held liable for any damages arising from the use of this software.
Permission is granted to anyone to use this software for any purpose, 
including commercial applications, and to alter it and redistribute it freely, 
subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
*/

#ifndef BT_DISPATCHER_H
#define BT_DISPATCHER_H
#include "../../LinearMath/btScalar.h"

class btCollisionAlgorithm;
struct btBroadphaseProxy;
class btRigidBody;
class btCollisionObject;
class btOverlappingPairCache;
struct btCollisionObjectWrapper;

class btPersistentManifold;
class btPoolAllocator;

struct btDispatcherInfo
{
	enum DispatchFunc
	{
		DISPATCH_DISCRETE = 1,
		DISPATCH_CONTINUOUS
	};
	btDispatcherInfo()
		: m_timeStep(btScalar(0.)),
		  m_stepCount(0),
		  m_dispatchFunc(DISPATCH_DISCRETE),
		  m_timeOfImpact(btScalar(1.)),
		  m_useContinuous(true),
		  m_enableSatConvex(false),
		  m_enableSPU(true),
		  m_useEpa(true),
		  m_allowedCcdPenetration(btScalar(0.04)),
		  m_useConvexConservativeDistanceUtil(false),
		  m_convexConservativeDistanceThreshold(0.0f),
		  m_deterministicOverlappingPairs(false)
	{
	}
	btScalar m_timeStep;
	int m_stepCount;
	int m_dispatchFunc;
	mutable btScalar m_timeOfImpact;
	bool m_useContinuous;
	bool m_enableSatConvex;
	bool m_enableSPU;
	bool m_useEpa;
	btScalar m_allowedCcdPenetration;
	bool m_useConvexConservativeDistanceUtil;
	btScalar m_convexConservativeDistanceThreshold;
	bool m_deterministicOverlappingPairs;
};

enum ebtDispatcherQueryType
{
	BT_CONTACT_POINT_ALGORITHMS = 1,
	BT_CLOSEST_POINT_ALGORITHMS = 2
};

#endif //BT_DISPATCHER_H