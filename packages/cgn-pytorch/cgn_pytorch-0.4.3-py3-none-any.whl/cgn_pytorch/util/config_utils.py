import os
import yaml
from importlib.resources import files

def load_config(checkpoint_dir=None, batch_size=None, num_points=None, data_path=None, arg_configs=[], save=False):
    """
    Loads yaml config file and overwrites parameters with function arguments and --arg_config parameters
    Arguments:
        checkpoint_dir {str} -- Checkpoint directory where config file was copied to
    Keyword Arguments:
        batch_size {int} -- [description] (default: {None})
        max_epoch {int} -- "epochs" (number of scenes) to train (default: {None})
        data_path {str} -- path to scenes with contact grasp data (default: {None})
        arg_configs {list} -- Overwrite config parameters by hierarchical command line arguments (default: {[]})
        save {bool} -- Save overwritten config file (default: {False})
    Returns:
        [dict] -- Config
    """
    if checkpoint_dir is None:
        checkpoint_dir = files('cgn_pytorch').joinpath('checkpoints')

    config_path = os.path.join(checkpoint_dir, 'config.yaml')
    config_path = config_path
    with open(config_path,'r') as f:
        global_config = yaml.safe_load(f)
        
    if batch_size is not None:
        global_config['data']['batch_size'] = int(batch_size)
    if num_points is not None:
        global_config['data']['num_points'] = int(num_points)
    
    if save:
        with open(os.path.join(checkpoint_dir, 'config.yaml'),'w') as f:
            yaml.dump(global_config, f)

    return global_config
