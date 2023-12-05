import os
import math
import timm
import torch
import numpy as np
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score
from utils_init import t2np, get_logp, load_weights
from datasets_init import create_test_data_loader
from models_init import positionalencoding2d, load_flow_model
from visualizer import plot_visualizing_results
from utils import calculate_pro_metric, convert_to_anomaly_scores, evaluate_thresholds
from config import parse_args
from utils import init_seeds
from PIL import Image
from torchvision import transforms as T

def validate(args, image_path, encoder, decoders):
    print('\nCompute loss and scores on category: {}'.format(args.class_name))
    
    decoders = [decoder.eval() for decoder in decoders]
    
    image_list, gt_label_list, gt_mask_list, file_names, img_types = [], [], [], [], []
    logps_list = [list() for _ in range(args.feature_levels)]
    with torch.no_grad():
        file_name = os.path.basename(image_path[:-4])
        transform_x = T.Compose([
                T.Resize(args.img_size, Image.ANTIALIAS),
                # T.CenterCrop(c.crop_size),
                T.ToTensor()])
        image = Image.open(image_path)
        normalize = T.Compose([T.Normalize(args.norm_mean, args.norm_std)])
        image = normalize(transform_x(image))
        
        if args.vis:
            image_list.extend(t2np(image))
            file_names.extend(file_name)
        
        image = image.to(args.device) # single scale
        features = encoder(image)  # BxCxHxW
        for l in range(args.feature_levels):
            e = features[l]  # BxCxHxW
            bs, dim, h, w = e.size()
            e = e.permute(0, 2, 3, 1).reshape(-1, dim)
            
            # (bs, 128, h, w)
            pos_embed = positionalencoding2d(args.pos_embed_dim, h, w).to(args.device).unsqueeze(0).repeat(bs, 1, 1, 1)
            pos_embed = pos_embed.permute(0, 2, 3, 1).reshape(-1, args.pos_embed_dim)
            decoder = decoders[l]

            if args.flow_arch == 'flow_model':
                z, log_jac_det = decoder(e)  
            else:
                z, log_jac_det = decoder(e, [pos_embed, ])

            logps = get_logp(dim, z, log_jac_det)  
            logps = logps / dim  
            logps_list[l].append(logps.reshape(bs, h, w))
            
    scores = convert_to_anomaly_scores(args, logps_list)
    # calculate detection AUROC
    img_scores = np.max(scores, axis=(1, 2))
    if args.vis:
        # img_threshold, pix_threshold = evaluate_thresholds(gt_label, gt_mask, img_scores, scores)
        # save_dir = os.path.join(args.output_dir, args.exp_name, 'vis_results', args.class_name)
        # save_dir = os.path.join('vis_results', args.class_name)
        save_dir = args.heatmap_path 
        os.makedirs(save_dir, exist_ok=True)
        plot_visualizing_results(image_list, scores, save_dir, file_names, args)

    
    return img_scores


def start_inference(device,gpu,image_path,encoder,decoders,input_size):

    # data loaders
    # test_loader = create_test_data_loader(args)
    args = parse_args()
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu
    if device == "GPU":
        args.device = torch.device("cuda")
        
    val_sample = Image.open(image_path)
    args.origin_size = val_sample.size
    # args.img_size = (args.inp_size, args.inp_size)  
    args.img_size = (input_size, input_size)  
    args.norm_mean, args.norm_std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]    
    args.img_dims = [3] + list(args.img_size)
    
    img_score = validate(args, image_path, encoder, decoders)
       
    return img_score

def load_model(device,gpu,checkpoint):
    init_seeds()
    args = parse_args()
    args.checkpoint = checkpoint
    
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu
    if device == "GPU":
        args.device = torch.device("cuda")
        
    encoder = timm.create_model(args.backbone_arch, features_only=True, 
                out_indices=[i+1 for i in range(args.feature_levels)], pretrained=True)
    encoder = encoder.to(args.device).eval()
    feat_dims = encoder.feature_info.channels()
    
    # Normalizing Flows
    decoders = [load_flow_model(args, feat_dim) for feat_dim in feat_dims]
    decoders = [decoder.to(args.device) for decoder in decoders]
    
    load_weights(encoder, decoders, args.checkpoint)
    
    return encoder,decoders
    