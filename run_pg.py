#!/usr/bin/env python
"""
This script runs a policy gradient algorithm
"""


from gym.envs import make
from modular_rl import *
import argparse, sys, cPickle
from tabulate import tabulate
import shutil, os, logging
import gym

def callback(stats):
    global COUNTER
    COUNTER += 1
    # Print stats
    print "*********** Iteration %i ****************" % COUNTER
    print tabulate(filter(lambda (k,v) : np.asarray(v).size==1, stats.items())) #pylint: disable=W0110
    # Store to hdf5
    if args.use_hdf:
        for (stat,val) in stats.items():
            if np.asarray(val).ndim==0:
                diagnostics[stat].append(val)
            else:
                assert val.ndim == 1
                diagnostics[stat].extend(val)
        if args.snapshot_every and ((COUNTER % args.snapshot_every==0) or (COUNTER==args.n_iter)):
            hdf['/agent_snapshots/%0.4i'%COUNTER] = np.array(cPickle.dumps(agent,-1))
    # Plot
    if args.plot:
        animate_rollout(env, agent, min(500, args.timestep_limit))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    update_argument_parser(parser, GENERAL_OPTIONS)
    parser.add_argument("--env", help="pusher, striker, thrower")
    parser.add_argument("--agent",required=True)
    parser.add_argument("--plot",action="store_true")
    args,_ = parser.parse_known_args([arg for arg in sys.argv[1:] if arg not in ('-h', '--help')])

    if args.env=="pusher":
        for i in range(100):
            env = make("Pusher-v%d"% i)
            env_spec = env.spec
            mondir = "/home/zhangc/POSEC/base_policy/Pusher/Pusher%d"% i + ".dir"
            if os.path.exists(mondir): shutil.rmtree(mondir)
            os.mkdir(mondir)
            env = gym.wrappers.Monitor(env, mondir, video_callable=None if args.video else VIDEO_NEVER)
            agent_ctor = get_agent_cls(args.agent)
            update_argument_parser(parser, agent_ctor.options)
            args = parser.parse_args()
            if args.timestep_limit == 0:
                args.timestep_limit = env_spec.timestep_limit
            cfg = args.__dict__
            np.random.seed(args.seed)
            agent = agent_ctor(env.observation_space, env.action_space, cfg)
            if args.use_hdf:
                hdf, diagnostics = prepare_h5_file(args,"/home/zhangc/POSEC/base_policy/Pusher/Pusher%d"% i)
            gym.logger.setLevel(logging.WARN)

            COUNTER = 0

            run_policy_gradient_algorithm(env, agent, callback=callback, usercfg = cfg)

            if args.use_hdf:
                hdf['env_id'] = env_spec.id
                try: hdf['env'] = np.array(cPickle.dumps(env, -1))
                except Exception: print "failed to pickle env" #pylint: disable=W0703
            env.close()

    elif args.env=="striker":
        for i in range(100):
            env = make("Striker-v%d"% i)
            env_spec = env.spec
            mondir = "/home/zhangc/POSEC/base_policy/Striker/Striker%d"% i + ".dir"
            if os.path.exists(mondir): shutil.rmtree(mondir)
            os.mkdir(mondir)
            env = gym.wrappers.Monitor(env, mondir, video_callable=None if args.video else VIDEO_NEVER)
            agent_ctor = get_agent_cls(args.agent)
            update_argument_parser(parser, agent_ctor.options)
            args = parser.parse_args()
            if args.timestep_limit == 0:
                args.timestep_limit = env_spec.timestep_limit
            cfg = args.__dict__
            np.random.seed(args.seed)
            agent = agent_ctor(env.observation_space, env.action_space, cfg)
            if args.use_hdf:
                hdf, diagnostics = prepare_h5_file(args,"/home/zhangc/POSEC/base_policy/Striker/Striker%d"% i)
            gym.logger.setLevel(logging.WARN)

            COUNTER = 0

            run_policy_gradient_algorithm(env, agent, callback=callback, usercfg = cfg)

            if args.use_hdf:
                hdf['env_id'] = env_spec.id
                try: hdf['env'] = np.array(cPickle.dumps(env, -1))
                except Exception: print "failed to pickle env" #pylint: disable=W0703
            env.close()

    elif args.env=="thrower":
        for i in range(100):
            env = make("Thrower-v%d"% i)
            env_spec = env.spec
            mondir = "/home/zhangc/POSEC/base_policy/Thrower/Thrower%d"% i + ".dir"
            if os.path.exists(mondir): shutil.rmtree(mondir)
            os.mkdir(mondir)
            env = gym.wrappers.Monitor(env, mondir, video_callable=None if args.video else VIDEO_NEVER)
            agent_ctor = get_agent_cls(args.agent)
            update_argument_parser(parser, agent_ctor.options)
            args = parser.parse_args()
            if args.timestep_limit == 0:
                args.timestep_limit = env_spec.timestep_limit
            cfg = args.__dict__
            np.random.seed(args.seed)
            agent = agent_ctor(env.observation_space, env.action_space, cfg)
            if args.use_hdf:
                hdf, diagnostics = prepare_h5_file(args,"/home/zhangc/POSEC/base_policy/Thrower/Thrower%d"% i)
            gym.logger.setLevel(logging.WARN)

            COUNTER = 0

            run_policy_gradient_algorithm(env, agent, callback=callback, usercfg = cfg)

            if args.use_hdf:
                hdf['env_id'] = env_spec.id
                try: hdf['env'] = np.array(cPickle.dumps(env, -1))
                except Exception: print "failed to pickle env" #pylint: disable=W0703
            env.close()

    else:
        print("Invalid argument")
